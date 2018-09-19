"""
test models
"""
from django.test import TestCase
from rest_framework.test import APIClient

from authors.apps.articles.models import Article, Tag
from authors.apps.authentication.models import User


# noinspection SpellCheckingInspection
class Tests(TestCase):

    def setUp(self):
        """
        test setup
        """
        User.objects.all().delete()
        Article.objects.all().delete()

        self.client = APIClient()
        self.user_name = "iroq"
        self.user_email = "iroq@sims.andela"
        self.password = "teamiroq1"

        self.title = "testing title"
        self.body = "testing body body"
        self.description = "description"
        self.tag1 = Tag.objects.create(tag_name="Django")
        self.tag1.save()
        self.tag2 = Tag.objects.create(tag_name="Django Restful")
        self.tag2.save()
        self.user = User.objects.create_user(
            self.user_name, self.user_email, self.password)
        self.user.save()

        self.article = Article.objects.create(
            author=self.user, title=self.title, description="", slug="ewfejdhgfdrtf")
        self.article.save()

    def test_articles_model(self):
        """Tests the creation of the Article model"""
        self.assertEqual(self.article.author.email, "iroq@sims.andela")
        self.assertEqual(self.article.__str__(), self.title)

    def test_tag_model(self):
        """Tests the creation of the Tag model"""
        self.assertEqual('Django', str(Tag.objects.all()[0]))

    def test_tags_on_article(self):
        """Tests the creation of the Article model with a Tag model added to it"""
        self.article.tags.add(self.tag1, self.tag2)
        self.assertEqual('Django', str(self.article.tags.all()[0]))
