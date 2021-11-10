from django.db import models


class BaseTag(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

    class Meta:
        abstract = True
        ordering = ['name']


class UserTag(BaseTag):
    pass


class AuthorTag(BaseTag):
    pass


class Article(models.Model):
    id = models.PositiveIntegerField(primary_key=True)
    url = models.URLField(null=True, blank=True)
    title = models.CharField(max_length=200, null=True, blank=True)
    published = models.DateTimeField(null=True, blank=True)
    user_tags = models.ManyToManyField(UserTag, blank=True)
    author_tags = models.ManyToManyField(AuthorTag, blank=True)
    words_count = models.PositiveIntegerField(null=True, blank=True)
    comments_count = models.PositiveIntegerField(null=True, blank=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-published']
