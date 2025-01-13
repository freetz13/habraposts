from django.urls import reverse
from rest_framework import serializers

from .models import Article, AuthorTag, UserTag


class UserTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserTag
        fields = "__all__"


class AuthorTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuthorTag
        fields = "__all__"


class ArticleSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    user_tags = serializers.SlugRelatedField(
        many=True, slug_field="name", queryset=UserTag.objects.all(), required=False
    )
    author_tags = serializers.SlugRelatedField(
        many=True, slug_field="name", queryset=AuthorTag.objects.all(), required=False
    )
    article_link = serializers.SerializerMethodField()

    class Meta:
        model = Article
        fields = [
            "id",
            "article_link",
            "url",
            "title",
            "published",
            "user_tags",
            "author_tags",
            "words_count",
            "comments_count",
        ]

    def get_article_link(self, object):
        url = reverse("article-detail", kwargs={"pk": object.id})
        request = self.context.get("request")
        return request.build_absolute_uri(url)

    def get_user_tags(self, object):
        return [tag.name for tag in object.user_tags.all()]

    def get_author_tags(self, object):
        return [tag.name for tag in object.author_tags.all()]

    def create(self, data):
        user_tags_data = data.pop("user_tags", [])
        author_tags_data = data.pop("author_tags", [])
        article = Article.objects.create(**data)

        # Добавляем теги
        new_user_tags = [
            UserTag.objects.get_or_create(name=tag_name)[0]
            for tag_name in user_tags_data
        ]
        article.user_tags.set(new_user_tags)

        new_author_tags = [
            AuthorTag.objects.get_or_create(name=tag_name)[0]
            for tag_name in author_tags_data
        ]
        article.author_tags.set(new_author_tags)
        return article

    def update(self, instance, data):
        user_tags_data = data.pop("user_tags", [])
        author_tags_data = data.pop("author_tags", [])

        instance.url = data.get("url", instance.url)
        instance.title = data.get("title", instance.title)
        instance.published = data.get("published", instance.published)
        instance.words_count = data.get("words_count", instance.words_count)
        instance.comments_count = data.get("comments_count", instance.comments_count)
        instance.save()

        # Обновляем user_tags, создавая их, если они не существуют
        new_user_tags = [UserTag.objects.get_or_create(name=tag_name)[0] for tag_name in user_tags_data]
        instance.user_tags.set(new_user_tags)

        # Обновляем author_tags, создавая их, если они не существуют
        new_author_tags = [AuthorTag.objects.get_or_create(name=tag_name)[0] for tag_name in author_tags_data]
        instance.author_tags.set(new_author_tags)

        return instance
