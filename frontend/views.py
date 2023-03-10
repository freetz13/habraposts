from django.views.generic import ListView

from api.models import Article


class PostList(ListView):
    model = Article
    context_object_name = "posts"
    paginate_by = 25
    template_name = "frontend/index.html"
