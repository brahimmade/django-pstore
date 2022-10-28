from django.urls import path

from . import views

urlpatterns = [
    path("all/", views.ListAllArticlesAPIView.as_view(), name="all-articles"),
    path("authors/", views.ListAuthorsArticleAPIView.as_view(), name="author-articles"),
    path("create/", views.create_article_api_view, name="article-create"),
    path(
        "details/<slug:slug>/",
        views.ArticleDetailView.as_view(),
        name="article-details",
    ),
    path("update/<slug:slug>/", views.update_article_api_view, name="update-article"),
    path("delete/<slug:slug>/", views.delete_article_api_view, name="delete-article"),
    path("search/", views.ArticleSearchAPIView.as_view(), name="article-search"),
]
