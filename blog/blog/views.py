import re

import logging
import markdown2 as markdown2
from django.core.paginator import Paginator
from django.shortcuts import render, render_to_response

# Create your views here.
from django.views.generic import DetailView
from django.views.generic import ListView
from rest_framework import generics

from blog.models import Article, Category, Quanzhifashi, Tag
from blog.serializers import ArticleSerializer

logger = logging.getLogger('django')


class IndexView(ListView):
    """
    首页视图,继承自ListVIew，用于展示从数据库中获取的文章列表
    """
    template_name = 'blog/index.html'
    context_object_name = 'article_list'  # context_object_name属性用于给上下文变量取名（在模板中使用该名字）
    paginate_by = 10
    article_list = Article.objects.filter(status='p').order_by('-created_time')  # 获取数据库中的所有已发布的文章，即filter(过滤)状态为'p'(已发布)的文章。
    category_list = Category.objects.all().order_by('name')

    def get_queryset(self):
        """
        过滤数据，获取所有已发布文章，并且将内容转成markdown形式
        :return: 需要展示的文章列表
        """

        # for article in self.article_list:
        #     if article.abstract:
        #         article.abstract = markdown2.markdown(article.abstract,
        #                                               extras=['fenced-code-blocks'])  # 将markdown标记的文本转为html文本
        return self.article_list

    def get_context_data(self, **kwargs):
        """
        增加额外的数据，这里返回一个文章分类，以字典的形式
        :param kwargs:
        :return:
        """
        context = super(IndexView, self).get_context_data(**kwargs)
        # kwargs['category_list'] = self.category_list
        context['category_list'] = self.category_list
        context['tags'] = Tag.objects.all()[0:20]
        return context


class ArticleDetailView(DetailView):
    """
    Django有基于类的视图DetailView,用于显示一个对象的详情页，我们继承它
    """
    model = Article  # 指定视图获取哪个 model
    template_name = 'blog/detail.html'
    context_object_name = 'article'  # 在模板中需要使用的上下文名字

    pk_url_kwarg = 'article_id'  # 用于接收一个来自url中的主键，然后会根据这个主键进行查询,我们之前在urlpatterns已经捕获article_id

    def get_object(self, queryset=None):
        """
        :param queryset: 如果有设置 queryset，该queryset 将用于对象的源
                        ,否则，将使用get_queryset(). get_object()从视图的所有参数中查找 pk_url_kwarg 参数；
        :return: 返回该视图要显示的对象。
        """
        obj = super(ArticleDetailView, self).get_object()
        obj.body = markdown2.markdown(obj.body, extras=['fenced-code-blocks'])
        return obj

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(ArticleDetailView, self).get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        t = context['article'].tags.all()
        # logger.debug(t.name)
        context['tags'] = context['article'].tags.all()
        return context


class CategoryView(ListView):
    """
    继承自ListView,用于展示一个列表
    """
    template_name = 'blog/index.html'  # 复用的是主页的模板
    context_object_name = 'article_list'

    def get_queryset(self):
        # 注意在url里我们捕获了分类的id作为关键字参数（cate_id）传递给了CategoryView，传递的参数在kwargs属性中获取
        article_list = Article.objects.filter(category=self.kwargs['cate_id'], status='p')
        for article in article_list:
            article.body = markdown2.markdown(article.body, extras=['fenced-code-blocks'])
        return article_list

    def get_context_data(self, **kwargs):
        """
        给视图增加额外的数据
        这里：增加一个category_list,用于在页面显示所有分类，按照名字排序
        :param kwargs:
        :return:
        """
        kwargs['category_list'] = Category.objects.all().order_by('name')
        return super(CategoryView, self).get_context_data(**kwargs)


class TagsView(ListView):
    template_name = 'blog/tags.html'
    context_object_name = 'tags'

    def get_queryset(self):
        tags = Tag.objects.all()
        return tags


def about(request):
    tags = Tag.objects.all()[0:20]
    return render_to_response('blog/about.html', context={'tags': tags})


def custom(req):
    ##
    ##
    # return HttpResponse("aa")
    return render_to_response('blog/custom.html', )


class QuanzhifashiView(ListView):
    """
    显示全职法师小说内容
    :param ListView:
    :return:
    """
    template_name = 'blog/story.html'
    context_object_name = 'article_list'
    quanzhifashi_list = Quanzhifashi.objects.all()

    def get_queryset(self):
        return self.quanzhifashi_list


class QuanzhifashiDetailView(DetailView):
    """
    Django有基于类的视图DetailView,用于显示一个对象的详情页，我们继承它
    """
    model = Quanzhifashi  # 指定视图获取哪个 model
    template_name = 'blog/detail.html'
    context_object_name = 'article'  # 在模板中需要使用的上下文名字

    pk_url_kwarg = 'article_id'  # 用于接收一个来自url中的主键，然后会根据这个主键进行查询,我们之前在urlpatterns已经捕获article_id


# api ---------------

class ArticleList(generics.ListCreateAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer


class ArticleDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
