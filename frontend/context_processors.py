from api.models import Article, AuthorTag, UserTag


def article_statistics(request):
    return {
        "articles_count": Article.objects.count(),
        "author_tags_count": AuthorTag.objects.count(),
        "user_tags_count": UserTag.objects.count(),
    }
