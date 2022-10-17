from django_countries.serializer_fields import CountryField
from django_countries.serializers import CountryFieldMixin
from rest_framework import serializers

from .models import Article, ArticleViews


class ArticleSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    country = CountryField(name_only=True)

    class Meta:
        model = Article
        exclude = []
        fields = [
            "id",
            "user",
            "title",
            "slug",
            "ref_code",
            "description",
            "country",
            "article_number",
            "price",
            "tax",
            "words",
            "total_words",
            "paragraphs",
            "subtitles",
            "keywords",
            "advert_type",
            "article_type",
            "cover_photo",
            "photo1",
            "photo2",
            "photo3",
            "photo4",
            "published_status",
            "views",
            "final_article_title"
        ]

    def get_user(self, obj):
        return obj.user.username


class ArticleCreateSerializer():
    country = CountryField(name_only=True)

    class Meta:
        model = Article
        exclude = ["updated_at", "pkid"]


class ArticleViewSerializer(serializers.ModelSerializer):
    class Meta:
        nodel = ArticleViews
        exclude = ["updated_at", "pkid"]
