import re
from urllib.parse import urlparse

import requests
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.views import Response

from habraparser import parse

from .models import Article, UserTag
from .serializers import ArticleSerializer, UserTagSerializer


@api_view(["GET"])
def article_info(request):
    url = request.GET.get("url")

    if re.match(r"\d+", str(url)):
        url = f"https://habr.com/post/{url}"

    # Prevent requests.exceptions.MissingSchema
    if not urlparse(url).scheme:
        url = f"https://{url}"

    response = requests.get(url)
    info = parse(response.content)

    return Response(info)


class ArticleViewSet(viewsets.ModelViewSet):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    permission_classes = []


class UserTagViewSet(viewsets.ModelViewSet):
    queryset = UserTag.objects.all()
    serializer_class = UserTagSerializer
    permission_classes = []
