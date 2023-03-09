from django.core.paginator import Paginator
from django.shortcuts import render

from api.models import Article


def index(request):
    articles = Article.objects.all()
    paginator = Paginator(articles, 25)  # Show 25 articles per page.

    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(
        request, "frontend/index.html", {"page_obj": page_obj}
    )
