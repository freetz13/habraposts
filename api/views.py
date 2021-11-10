import re
from urllib.parse import urlparse

import requests
from rest_framework.decorators import api_view
from rest_framework.views import Response

from habraparser import parse


@api_view(['GET'])
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
