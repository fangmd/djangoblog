from django.conf.urls import url

from blog.views import IndexView, ArticleDetailView, CategoryView, custom, ArticleList, ArticleDetail, TagsView, about

urlpatterns = [

    # 首页调用IndexView
    url(r'^$', IndexView.as_view(), name='index'),
    url(r'^index.html/$', IndexView.as_view(), name='index'),  # .html 处理方式不对哦

    # 使用(?P<>\d+)的形式捕获值给<>中得参数，比如(?P<article_id>\d+)，当访问/blog/article/3时，
    # 将会将3捕获给article_id,这个值会传到views.ArticleDetailView,这样我们就可以判断展示哪个Article了
    url(r'article/(?P<article_id>\d+)$', ArticleDetailView.as_view(), name='detail'),
    url(r'category/(?P<cate_id>\d+)$', CategoryView.as_view(), name='category'),
    url(r'^custom/$', custom),
    url(r'^tags/$', TagsView.as_view(), name='tags'),
    url(r'^about/$', about, name='about'),

    # api
    url(r'api/v1/articles$', ArticleList.as_view()),
    url(r'api/v1/articles/(?P<article_id>\d+)$', ArticleDetail.as_view()),

]
