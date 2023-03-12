from django.views.generic import DeleteView, ListView

from api.models import Article


class PostList(ListView):
    model = Article
    context_object_name = "posts"
    paginate_by = 25
    template_name = "frontend/index.html"


class PostDelete(DeleteView):
    model = Article
    template_name = "frontend/delete.html"
    success_url = "/"
