from django.test import TestCase
from api.models import Article, AuthorTag, UserTag


class OrphansTestCase(TestCase):
    def setUp(self):
        AuthorTag.objects.create(name="python")
        UserTag.objects.create(name="python")
        Article.objects.create(id=1234, title="Writing Python scripts the right way")
        Article.objects.create(id=4321, title="Writing Python scripts the wrong way")

    def test_if_no_author_tags_orphans_after_deleting_articles(self):
        tag_python = AuthorTag.objects.get(name="python")

        article_1 = Article.objects.get(title="Writing Python scripts the right way")
        article_1.author_tags.add(tag_python)

        article_2 = Article.objects.get(title="Writing Python scripts the wrong way")
        article_2.author_tags.add(tag_python)

        article_1.delete()
        self.assertEqual(AuthorTag.objects.count(), 1, "There should be exactly 1 tag")

        article_2.delete()
        self.assertEqual(AuthorTag.objects.count(), 0, "There should be no tags")

    def test_if_no_user_tags_orphans_after_deleting_articles(self):
        tag_python = UserTag.objects.get(name="python")

        article_1 = Article.objects.get(title="Writing Python scripts the right way")
        article_1.user_tags.add(tag_python)

        article_2 = Article.objects.get(title="Writing Python scripts the wrong way")
        article_2.user_tags.add(tag_python)

        article_1.delete()
        self.assertEqual(UserTag.objects.count(), 1, "There should be exactly 1 tag")

        article_2.delete()
        self.assertEqual(UserTag.objects.count(), 0, "There should be no tags")
