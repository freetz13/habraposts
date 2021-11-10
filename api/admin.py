from django.contrib import admin
from django.utils.html import format_html

from .models import Article, AuthorTag, UserTag


class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'link', 'published', 'comments_count', 'words_count')
    search_fields = ['title']

    def link(self, obj):
        return format_html(f"<a href='{obj.url}' target='_blank'>🔗</a>")


admin.site.register(UserTag)
admin.site.register(AuthorTag)
admin.site.register(Article, ArticleAdmin)
