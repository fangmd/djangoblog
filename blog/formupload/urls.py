from django.conf.urls import url

import formupload
from blog.views import IndexView, ArticleDetailView, CategoryView, custom
from formupload import views
from formupload.views import get_file

urlpatterns = [
    url(r'name/$', views.get_name, name='name'),
    url(r'upload/$', get_file, name='name'),
    url(r'thanks/$', views.FileUploadResult.as_view(), name='name')
]
