from django.shortcuts import render
from api.models import Article

def index(request):
    articles = Article.objects.all()[:50]
    return render(request, "frontend/index.html", {"articles": articles})