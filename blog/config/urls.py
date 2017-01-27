"""blog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.conf import settings
from django.views.static import serve
from django.conf.urls.static import static

from blog.views import QuanzhifashiView, QuanzhifashiDetailView

urlpatterns = [
    url(r'^admin/', admin.site.urls),

    # 其中namespace参数为我们指定了命名空间，这说明这个urls.py中的url是blog app下的，这样即使不同的app下有相同url也不会冲突了。
    url(r'^blog/', include('blog.urls', namespace='blog', app_name='blog')),

    url(r'^form/', include('formupload.urls', namespace='form', app_name='formupload')),

    # 爬虫小说
    url(r'^spider/$', QuanzhifashiView.as_view(), name='spider'),
    url(r'^spider/article/(?P<article_id>\d+)$', QuanzhifashiDetailView.as_view(), name='spiderdetail'),

    # api
    # url(r'^api/v1/')

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# ... the rest of your URLconf goes here ...

if settings.DEBUG:
    urlpatterns += [
        url(r'^media/(?P<path>.*)$', serve, {
            'document_root': settings.MEDIA_ROOT,
        }),
    ]
