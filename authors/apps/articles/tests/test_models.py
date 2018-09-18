"""
test models
"""
from django.test import TestCase
from rest_framework.test import APIClient

from authors.apps.articles.models import Article
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

    def test_articles_model(self):
        user = User.objects.create_user(self.user_name, self.user_email, self.password)
        user.save()
        article = Article.objects.create(author=user, title=self.title, description="", slug="ewfejdhgfdrtf")
        article.save()
        self.assertEqual(article.author.email, "iroq@sims.andela")
        self.assertEqual(article.__str__(), self.title)
