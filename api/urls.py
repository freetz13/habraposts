from django.urls import path

from .views import article_info

urlpatterns = [
    path('article_info/', article_info),
]
