"""This module tests the authentication model."""
from django.test import TestCase
from authors.apps.authentication.models import User
from authors.apps.authentication.tests.base_test import BaseTest


class ModelTestCase(TestCase, BaseTest):
    """This class defines the test suite for the user model."""

    def setUp(self):
        """Define the test client and other test variables."""
        BaseTest.__init__(self)
        self.user = User.objects.create_user(self.user_name, self.user_email)

    def test_model_can_create_a_user(self):
        """Test the user model can create a user."""
        self.assertEqual(self.user.username, "iroq")
        self.assertEqual(self.user.email, "iroq@sims.andela")
        self.assertEqual(1, User.objects.count())

    def test_getting_short_name_full_name(self):
        """Test the return of a short name and a full name."""
        self.assertEqual("iroq", self.user.get_full_name)
        self.assertEqual("iroq", self.user.get_short_name())
