from rest_framework import serializers

from blog.models import Article


class BaseSerializer(object):
    email = serializers.EmailField()

    class Meta:
        read_only_fields = ('account_name',)


class ArticleSerializer(BaseSerializer, serializers.ModelSerializer):
    # created = serializers.DateTimeField()

    class Meta:
        model = Article
        fields = '__all__'
        # fields = ('id', 'title')

