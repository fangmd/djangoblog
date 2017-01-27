from django.contrib import admin

# Register your models here.
from blog.models import Article, Category, Quanzhifashi

admin.site.register(Article)
admin.site.register(Category)
admin.site.register(Quanzhifashi)
