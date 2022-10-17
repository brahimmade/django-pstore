from django.contrib import admin

from .models import Article, ArticleViews


# Register your models here.
class ArticleAdmin(admin.ModelAdmin):
    list_display = ["title", "country", "advert_type", "article_type"]
    list_filter = ["advert_type", "article_type", "country"]


admin.site.register(Article, ArticleAdmin)
admin.site.register(ArticleViews)
