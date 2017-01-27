import markdown2
from django.db import models

# Create your models here.
from django.views.generic import DetailView


class Article(models.Model):
    """
    文章类:标题，正文，创建时间，修改时间，文章状态，摘要，游览量，点赞数，置顶，分类
    """

    STATUS_CHOICES = (
        ('d', 'Draft'),
        ('p', 'Published')
    )

    title = models.CharField('标题', max_length=70)  # 标题 是位置参数 verbose_name ？？？？
    body = models.TextField('正文')
    created_time = models.DateTimeField('创建时间', auto_now_add=True)  # TODO: 需要自定义
    last_modified_time = models.DateTimeField('修改时间', auto_now_add=True)
    status = models.CharField('文章状态', max_length=1, choices=STATUS_CHOICES)
    abstract = models.CharField('摘要', max_length=54, blank=True, null=True, help_text='可选，如过为空取文章的前54个字符')
    views = models.PositiveIntegerField('游览量', default=0)
    likes = models.PositiveIntegerField('点赞数', default=0)
    topped = models.BooleanField('置顶', default=False)

    # 文章的分类，ForeignKey即数据库中的外键。
    # 外键的定义是：如果数据库中某个表的列的值是另外一个表的主键。外键定义了一个一对多的关系，这里即一篇文章对应一个分类，而一个分类下可能有多篇
    # 文章。详情参考django官方文档关于ForeinKey的说明，on_delete=models.SET_NULL表示删除某个分类（category）后该分类下所有的Article的外键设为null（空）
    category = models.ForeignKey('Category', verbose_name='分类', null=True, on_delete=models.SET_NULL)
    tags = models.ManyToManyField('Tag', verbose_name='标签', null=True)

    def __str__(self):
        """
        主要用于交互解释器显示表示该类的字符串
        :return:
        """
        return self.title

    class Meta:
        """
        Meta 包含一系列选项，这里的 ordering 表示排序，- 号表示逆序。即当从数据库中取出文章时，其是按文章最后一次修改时间逆序排列的。
        """

        ordering = ['-last_modified_time']


class Category(models.Model):
    """
    分类：类名，创建时间，修改时间
    """

    name = models.CharField('类名', max_length=20)
    create_time = models.DateTimeField('创建时间', auto_now_add=True)
    last_modified_time = models.DateTimeField('修改时间', auto_now_add=True)

    def __str__(self):
        return self.name


class Tag(models.Model):
    """
    Tags
    """
    name = models.CharField('标签名', max_length=20, unique=True)

    def __str__(self):
        return self.name


class Quanzhifashi(models.Model):
    """
    全职法师小说类
    """
    name = models.CharField("章节", max_length=30)
    url = models.CharField("url", max_length=30)
    body = models.TextField("正文", default=" NULL")

    def __str__(self):
        return self.name
