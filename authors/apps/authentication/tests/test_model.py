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
        self.superuser = User.objects.create_superuser(
            self.superuser_name, self.superuser_email, self.superuserpassword)

    def test_model_can_create_a_user(self):
        """Test the user model can create a user."""
        self.assertEqual(self.user.username, "iroq")
        self.assertEqual(self.user.email, "iroq@sims.andela")
        self.assertEqual(self.user_email, str(
            User.objects.get(username="iroq")))

    def test_getting_short_name_full_name(self):
        """Test the return of a short name and a full name."""
        self.assertEqual("iroq", self.user.get_full_name)
        self.assertEqual("iroq", self.user.get_short_name())

    def test_model_can_create_a_superuser(self):
        """Test the user model can create a user."""

        self.assertEqual(self.superuser_email, str(
            User.objects.get(username='iroquois')))

    def test_missing_username(self):
        """Test that an error is returned when a username is not provided."""

        try:
            User.objects.create_user(None, self.user.email)
        except TypeError as error:
            self.assertEqual(str(error), "Users must have a username.")

    def test_missing_email_address(self):
        """Test that an error is return when an email address is not provided."""

        try:
            User.objects.create_user(self.user_name, None)
        except TypeError as error:
            self.assertEqual(str(error), "Users must have an email address.")

    def test_superuser_missing_password(self):
        """
        Test that an error is return when a password is missing on creating
        a superuser.
        """

        try:
            User.objects.create_superuser(
                self.user_name, self.user_email, None)
        except TypeError as error:
            self.assertEqual(str(error), "Superusers must have a password.")

    def test_token_creation(self):
        """
        Test that a token is created upon creating a user.
        """

        self.assertTrue(self.user.token)
        self.assertTrue(self.superuser.token)
        self.assertGreater(len(self.user.token), 10)
