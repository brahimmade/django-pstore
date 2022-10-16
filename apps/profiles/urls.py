from django.urls import path

from .views import (AuthorListAPIView, GetProfileAPIView,
                    TopAuthorsListAPIView, UpdateProfileAPIView)

urlpatterns = [
    path("me/", GetProfileAPIView.as_view(), name="get_profile"),
    path("update/<str:username>/", UpdateProfileAPIView.as_view(), name="update_profile"),
    path("authors/all/", AuthorListAPIView.as_view(), name="all-authors"),
    path("top-authors/all/", TopAuthorsListAPIView.as_view(), name="top-authors"),
]
