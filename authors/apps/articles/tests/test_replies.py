from django.test import TestCase
import json
from authors.apps.articles.models import Comments
from authors.apps.authentication.models import User
from rest_framework.test import APIClient
from rest_framework import status
from .test_replies_data import TestDataReplies


class Tests(TestCase, TestDataReplies):

    def setUp(self):
        """
        setup tests
        """
        User.objects.all().delete()
        Comments.objects.all().delete()

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

    def test_post_new_reply_on_comment(self):
        """first post an article """
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

        response = self.client.post(
            "/api/articles/{}/comment/".format(slug), data=json.dumps(
                self.post_comment), content_type='application/json')
        self.assertEqual(201, response.status_code)
        self.assertIsInstance(response.json(), dict)

        id = response.json().get('id')
        response = self.client.post(
            "/api/articles/comment/{}/replies/".format(id), data=json.dumps(
                self.post_reply), content_type='application/json')
        self.assertEqual(201, response.status_code)
        self.assertIsInstance(response.json(), dict)

    def test_post_empty_reply(self):

        """post empty reply """
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

        response = self.client.post(
            "/api/articles/{}/comment/".format(slug), data=json.dumps(
                self.post_comment), content_type='application/json')
        self.assertEqual(201, response.status_code)
        self.assertIsInstance(response.json(), dict)

        id = response.json().get('id')

        response = self.client.post(
            "/api/articles/comment/{}/replies/".format(id), data=json.dumps(
                self.post_missing_reply), content_type='application/json')
        self.assertEqual(400, response.status_code)

    def test_reply_non_existing_comment_id(self):
        """post reply  with non existing commentID """
        commentid = 99
        response = self.client.post(
            "/api/articles/comment/{}/replies/".format(commentid), data=json.dumps(
                self.post_reply), content_type='application/json')
        self.assertEqual(404, response.status_code)

    def test_update_reply(self):
        """test Update comment"""
        """first post an article """
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

        response = self.client.post(
            "/api/articles/{}/comment/".format(slug), data=json.dumps(
                self.post_comment), content_type='application/json')
        self.assertEqual(201, response.status_code)
        self.assertIsInstance(response.json(), dict)

        id = response.json().get('id')
        response = self.client.post(
            "/api/articles/comment/{}/replies/".format(id), data=json.dumps(
                self.post_update_reply), content_type='application/json')
        self.assertEqual(201, response.status_code)
        self.assertIsInstance(response.json(), dict)

        reply_id = response.json().get('id')

        response = self.client.put(
            "/api/articles/comment/replies/{}/".format(reply_id), data=json.dumps(
                self.post_reply), content_type='application/json')
        self.assertEqual(200, response.status_code)
        self.assertIsInstance(response.json(), dict)

    def test_reply_update_with_no_content(self):
        """first post an article """
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

        response = self.client.post(
            "/api/articles/{}/comment/".format(slug), data=json.dumps(
                self.post_comment), content_type='application/json')
        self.assertEqual(201, response.status_code)
        self.assertIsInstance(response.json(), dict)

        id = response.json().get('id')

        response = self.client.put(
            "/api/articles/comment/{}/".format(id), data=json.dumps(
                self.post_comment), content_type='application/json')
        self.assertEqual(200, response.status_code)
        self.assertIsInstance(response.json(), dict)

        id = response.json().get('id')
        response = self.client.post(
            "/api/articles/comment/{}/replies/".format(id), data=json.dumps(
                self.post_reply), content_type='application/json')
        self.assertEqual(201, response.status_code)
        self.assertIsInstance(response.json(), dict)

        reply_id = response.json().get('id')
        response = self.client.put(
            "/api/articles/comment/replies/{}/".format(reply_id), data=json.dumps(
                self.post_update_no_body), content_type='application/json')
        self.assertEqual(400, response.status_code)
        self.assertIsInstance(response.json(), dict)

    def test_delete_reply(self):

        """test delete comment"""
        """first post an article """
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

        response = self.client.post(
            "/api/articles/{}/comment/".format(slug), data=json.dumps(
                self.post_comment), content_type='application/json')
        self.assertEqual(201, response.status_code)
        self.assertIsInstance(response.json(), dict)
        id = response.json().get('id')
        response = self.client.post(
            "/api/articles/comment/{}/replies/".format(id), data=json.dumps(
                self.post_reply), content_type='application/json')
        self.assertEqual(201, response.status_code)
        self.assertIsInstance(response.json(), dict)

        reply_id = response.json().get('id')
        response = self.client.delete(
            "/api/articles/comment/replies/{}/".format(reply_id), content_type='application/json')
        self.assertEqual(204, response.status_code)

    def test_delete_reply_with_a_non_existing_id(self):

        """delete a Reply with a non existing ID"""
        reply_id = 1000
        response = self.client.delete(
            "/api/articles/comment/replies/{}/".format(reply_id), content_type='application/json')
        self.assertEqual(404, response.status_code)















