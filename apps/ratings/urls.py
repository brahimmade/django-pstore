from django.urls import path
from . import views

urlpatterns = [
    path("<str:profile_id>/", views.create_author_review, name="create-rating")
]
