from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import ArticleViewSet, UserTagViewSet, article_info

router = DefaultRouter()
router.register(r"articles", ArticleViewSet)
router.register(r"user_tags", UserTagViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path("article_info/", article_info),
]
