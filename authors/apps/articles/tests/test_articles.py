"""
Test articles
"""
import json

from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from authors.apps.articles.models import Article, Tag
from authors.apps.authentication.models import User
from .test_data import TestData


class Tests(TestCase, TestData):

    def setUp(self):
        """
        setup tests
        """
        User.objects.all().delete()
        Article.objects.all().delete()

        self.login_data = {"user": {"email": self.user_email, "password": self.password,
                                    }
                           }
        self.user_data = {"user": {"username": self.user_name, "email": self.user_email,
                                   "password": self.password,
                                   }
                          }
        self.client = APIClient()

        self.response = self.client.post(
            "/api/users/",
            self.user_data,
            format="json")
        self.user = User.objects.get(email=self.user_email)
        self.user.is_active = True
        self.user.is_email_verified = True
        self.user.save()
        self.response = self.client.post(
            "/api/users/login/",
            self.login_data,
            format="json")
        self.assertEqual(status.HTTP_200_OK, self.response.status_code)
        self.assertIn('token', self.response.data)
        token = self.response.data.get("token", None)
        self.client.credentials(HTTP_AUTHORIZATION="Token {0}".format(token))

    def test_post_new_article(self):
        response = self.client.post(
            "/api/articles/", data=json.dumps(
                self.post_article), content_type='application/json')
        self.assertEqual(201, response.status_code)
        self.assertIn('article', response.json())
        self.assertIsInstance(response.json().get("article"), dict)

    def test_post_article_missing_data(self):
        response = self.client.post(
            "/api/articles/", data=json.dumps(
                self.post_article_missing_data), content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertIn('errors', response.json())

    def test_list_zero_article(self):
        response = self.client.get(
            "/api/articles/", content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertIn('article', response.json())
        self.assertIsInstance(response.json().get("article"), dict)

    def test_list_one_article(self):
        response = self.client.post(
            "/api/articles/", data=json.dumps(
                self.post_article), content_type='application/json')
        self.assertEqual(response.status_code, 201)
        self.assertIn('article', response.json())
        self.assertIsInstance(response.json().get("article"), dict)

        response = self.client.get(
            "/api/articles/", content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertIn('article', response.json())
        self.assertIsInstance(response.json().get("article"), dict)

        # test for invalid query params
        response = self.client.get(
            "/api/articles/?offset=3&limit=3e", content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertIn('article', response.json())

    def test_list_specific_article(self):
        response = self.client.post(
            "/api/articles/", data=json.dumps(
                self.post_article), content_type='application/json')
        self.assertEqual(response.status_code, 201)
        self.assertIn('article', response.json())
        self.assertIsInstance(response.json().get("article"), dict)

        response = self.client.get(
            "/api/articles/", content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertIn('article', response.json())
        self.assertIsInstance(response.json().get("article"), dict)

        slug = response.json().get("article").get("results").get("slug")

        response = self.client.get(
            "/api/articles/{0}/".format(slug), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertIn('article', response.json())
        self.assertIsInstance(response.json().get("article"), dict)

    def test_delete_specific_article(self):
        response = self.client.post(
            "/api/articles/", data=json.dumps(
                self.post_article), content_type='application/json')
        self.assertEqual(response.status_code, 201)
        self.assertIn('article', response.json())
        self.assertIsInstance(response.json().get("article"), dict)

        response = self.client.get(
            "/api/articles/", content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertIn('article', response.json())
        self.assertIsInstance(response.json().get("article"), dict)

        slug = response.json().get("article").get("results").get("slug")

        response = self.client.delete(
            "/api/articles/{0}/".format(slug), content_type='application/json')
        self.assertEqual(response.status_code, 204)
        self.assertIn('detail', response.data)
        self.assertIsInstance(response.data.get("detail"), str)

    def test_delete_not_found_article(self):
        response = self.client.delete(
            "/api/articles/54/", content_type='application/json')
        self.assertEqual(response.status_code, 404)
        self.assertIn('detail', response.data)
        self.assertIsInstance(response.data.get("detail"), str)

    def test_list_many_articles(self):
        val = 0
        while val < 3:
            response = self.client.post(
                "/api/articles/", data=json.dumps(
                    self.post_article), content_type='application/json')
            self.assertEqual(response.status_code, 201)
            self.assertIn('article', response.json())
            self.assertIsInstance(response.json().get("article"), dict)
            val += 1

        response = self.client.get(
            "/api/articles/", content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json().get(
            "articles").get("results"), list)
        self.assertEqual(len(response.json().get("articles")), 3)

    def test_update_article(self):
        response = self.client.post(
            "/api/articles/", data=json.dumps(
                self.post_article), content_type='application/json')
        self.assertEqual(response.status_code, 201)
        self.assertIn('article', response.json())
        self.assertIsInstance(response.json().get("article"), dict)

        response = self.client.get(
            "/api/articles/", content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertIn('article', response.json())
        self.assertIsInstance(response.json().get("article"), dict)

        slug = response.json().get("article").get("results").get("slug")

        response = self.client.put(
            "/api/articles/{0}/".format(slug), data=json.dumps(
                self.update_article), content_type='application/json')
        self.assertEqual(response.status_code, 202)
        self.assertIn('article', response.json())
        self.assertIsInstance(response.json().get("article"), dict)

    def test_update_article_missing_data_and_not_exist(self):
        response = self.client.post(
            "/api/articles/", data=json.dumps(
                self.post_article), content_type='application/json')
        self.assertEqual(response.status_code, 201)
        self.assertIn('article', response.json())
        self.assertIsInstance(response.json().get("article"), dict)

        response = self.client.get(
            "/api/articles/", content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertIn('article', response.json())
        self.assertIsInstance(response.json().get("article"), dict)

        slug = response.json().get("article").get("results").get("slug")

        response = self.client.put(
            "/api/articles/{0}/".format(slug), data=json.dumps(
                self.post_article_missing_data), content_type='application/json')
        self.assertEqual(response.status_code, 202)
        self.assertIn('article', response.json())
        self.assertIsInstance(response.json().get("article"), dict)

        # test article does not exist
        response = self.client.put(
            "/api/articles/45/", data=json.dumps(
                self.post_article_missing_data), content_type='application/json')
        self.assertEqual(response.status_code, 404)
        self.assertIn('article', response.json())
        self.assertIsInstance(response.json().get("article"), dict)

    def test_article_created_with_tag(self):
        """
        Tests the creation of an article with tags. 
        """
        response = self.client.post(
            "/api/articles/",
            self.post_article_with_tags,
            format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual('django', response.data['tagList'][0])

    def test_view_returns_tag_list(self):
        """
        Tests that a list of tags is returned by the TagViewSet view
        """
        self.user.is_superuser = True
        self.user.save()
        self.client.post(
            "/api/articles/tags/tag_list/",
            self.post_tag,
            format="json")
        response = self.client.get("/api/articles/tags/tag_list/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("tags", response.json())
        self.assertEqual('django', response.json()['tags'][0]['tag_name'])

    def test_view_updates_tag(self):
        """
        Tests an update of a tag
        """
        self.user.is_superuser = True
        self.user.save()
        self.client.post(
            "/api/articles/tags/tag_list/",
            self.post_tag,
            format="json")
        resp = self.client.get("/api/articles/tags/tag_list/")
        tag_id = resp.json()['tags'][0]['id']
        response = self.client.put("/api/articles/tags/tag_list/{}/".format(tag_id),
                                   self.update_tag,
                                   format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual("django_restful", response.json()['tag']['tag_name'])

    def test_view_deletes_tag(self):
        """
        Test the delete of a tag
        """
        self.user.is_superuser = True
        self.user.save()
        self.client.post(
            "/api/articles/tags/tag_list/",
            self.post_tag,
            format="json")
        resp = self.client.get("/api/articles/tags/tag_list/")
        tag_id = resp.json()['tags'][0]['id']
        response = self.client.delete(
            "/api/articles/tags/tag_list/{}/".format(tag_id))
        after_delete_resp = self.client.get(
            "/api/articles/tags/tag_list/{}/".format(tag_id))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual("Not found.", after_delete_resp.json()[
            'tag']['detail'])

    def test_no_superuser_permissions(self):
        """
        Tests that a TagViewSet is not accessed by an 
        individual who is not a super user
        """
        response = self.client.post(
            "/api/articles/tags/tag_list/",
            self.post_tag,
            format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual("You do not have permission to perform this action.",
                         response.json()["tag"]["detail"])

    def test_tag_update_on_article(self):
        """Test that a tag is updated on an article"""
        self.client.post(
            "/api/articles/",
            self.post_article_with_tags,
            format="json")
        resp = self.client.get("/api/articles/")
        slug = resp.json()["article"]["results"]["slug"]

        response = self.client.put(
            "/api/articles/{}/".format(slug),
            self.update_tag_on_article_data,
            format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)
        self.assertIn("django_restful", response.json()["article"]["tagList"])
        self.assertNotIn("django", response.json()["article"]["tagList"])

    def test_reporting_an_article(self):
        """Test that a user is able to report an article"""
        self.client.post(
            "/api/articles/",
            self.post_article_with_tags,
            format="json")
        resp = self.client.get("/api/articles/")
        slug = resp.json()["article"]["results"]["slug"]
        response = self.client.post(
            "/api/articles/reports/{}/".format(slug),
            self.post_report,
            format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual("for real I have nothing to report.",
                         response.json()["report_message"])

    def test_reporting_on_non_existing_article(self):
        """
        Test that an error is raised when a user tries to 
        report an article that does not exist.
        """
        response = self.client.post(
            "/api/articles/reports/wrong_slug/",
            self.post_report,
            format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual("An article with this slug does not exist",
                         response.json()["detail"])

    def test_report_message_validation(self):
        """
        Test that an error is raised when the request is 
        missing: {"report_message": "the report message here"} or 
        has a blank report message.
        """
        self.client.post(
            "/api/articles/",
            self.post_article_with_tags,
            format="json")
        resp = self.client.get("/api/articles/")
        slug = resp.json()["article"]["results"]["slug"]
        response = self.client.post(
            "/api/articles/reports/{}/".format(slug),
            " ",
            format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual("A report message is required",
                         response.json()["detail"])

    def test_all_reports_returned(self):
        """Test that all reports on all articles are returned."""
        self.user.is_superuser = True
        self.user.save()
        self.client.post(
            "/api/articles/",
            self.post_article_with_tags,
            format="json")
        resp = self.client.get("/api/articles/")
        slug = resp.json()["article"]["results"]["slug"]
        self.client.post(
            "/api/articles/reports/{}/".format(slug),
            self.post_report,
            format="json"
        )

        response = self.client.get("/api/articles/reports/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual("for real I have nothing to report.",
                         response.json()["reports"][0]["report_message"])

    def test_reports_of_a_single_article_returned(self):
        """Test that all reports of a single article are returned."""
        self.user.is_superuser = True
        self.user.save()
        self.client.post(
            "/api/articles/",
            self.post_article_with_tags,
            format="json")
        resp = self.client.get("/api/articles/")
        slug = resp.json()["article"]["results"]["slug"]
        self.client.post(
            "/api/articles/reports/{}/".format(slug),
            self.post_report,
            format="json"
        )

        response = self.client.get("/api/articles/reports/{}/".format(slug))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual("for real I have nothing to report.",
                         response.json()["reports"][0]["report_message"])

    def test_non_superuser_denied_report_viewing(self):
        """
        Test that an error is returned when a non super user tries to
        view reports made on articles
        """
        response = self.client.get("/api/articles/reports/")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual("permission denied, you do not have access rights.",
                         response.json()["detail"])
