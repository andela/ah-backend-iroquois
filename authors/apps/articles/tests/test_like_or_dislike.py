from django.test import TestCase
from rest_framework.test import APIClient
from authors.apps.articles.models import User
import json


class LikeOrDislikeTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

        # create first user
        self.first_user = User.objects.create_user(
            "username_one", "first_email@gmail.com", "password"
        )
        self.first_user = User.objects.get(email="first_email@gmail.com")
        self.first_user.is_active = True
        self.first_user.is_email_verified = True
        self.first_user.save()

        # create second user
        self.second_user = User.objects.create_user(
            "username_two", "second_email@gmail.com", "password"
        )
        self.second_user = User.objects.get(email="second_email@gmail.com")
        self.second_user.is_active = True
        self.second_user.is_email_verified = True
        self.second_user.save()

        # create_third user
        self.third_user = User.objects.create_user(
            "username_three", "third_email@gmail.com", "password"
        )
        self.third_user = User.objects.get(email="third_email@gmail.com")
        self.third_user.is_active = True
        self.third_user.is_email_verified = True
        self.third_user.save()

        # Login first user
        self.login_first = self.client.post("/api/users/login/",
                                            data={"user": {
                                                "email": "first_email@gmail.com",
                                                "password": "password",
                                                }
                                            },
                                            format="json")

        # Login second user
        self.login_second = self.client.post("/api/users/login/",
                                            data={"user": {
                                                "email": "second_email@gmail.com",
                                                "password": "password",
                                                }
                                            },
                                            format="json")

        # Login third user
        self.login_third = self.client.post("/api/users/login/",
                                            data={"user": {
                                                "email": "third_email@gmail.com",
                                                "password": "password",
                                                }
                                            },
                                            format="json")
        self.post_article = {
            "article": {
                "title": "Yet another Sand Blog",
                "description": "Sand is m testing",
                "body": "another that am doin test"
            }
        }

        self.first_like = {"message": "You like this article"}
        self.re_like = {"message": "You no longer like this article"}

        self.first_dislike = {"message": "You dislike this article"}
        self.re_dislike = {"message": "You no longer dislike this article"}

        self.like_to_dislike = {'message': 'You now dislike this article'}
        self.dislike_to_like = {'message': 'You now like this article'}

        self.article_404 = {'detail': 'Article is not found.'}

    def test_like_or_dislike_article(self):
        token = self.login_first.data['token']
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        response = self.client.post(
            "/api/articles/", data=json.dumps(
                self.post_article), content_type='application/json')
        self.assertEqual(201, response.status_code)
        self.assertIn('article', response.json())
        self.assertIsInstance(response.json().get("article"), dict)

        # get slug from created article
        self.slug = response.json()['article']['slug']

        # let username_one like this article
        self.first_like_response = self.client.post("/api/articles/{}/like/".format(self.slug))
        self.assertEqual(self.first_like_response.json(), self.first_like)

        # let username_one re like this article
        self.first_like_response = self.client.post("/api/articles/{}/like/".format(self.slug))
        self.assertEqual(self.first_like_response.json(), self.re_like)

        # Let username_two like this article
        token = self.login_second.data['token']
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        self.second_like_response = self.client.post("/api/articles/{}/like/".format(self.slug))
        self.assertEqual(self.second_like_response.json(), self.first_like)

        # lets username_two dislike the article he previously liked
        self.first_like_response = self.client.post("/api/articles/{}/dislike/".format(self.slug))
        self.assertEqual(self.first_like_response.json(), self.like_to_dislike)

        # Let username_two re dislike this article
        self.first_like_response = self.client.post("/api/articles/{}/dislike/".format(self.slug))
        self.assertEqual(self.first_like_response.json(), self.re_dislike)

        # lets username_two dislike the article | remember it is in the default state
        self.first_like_response = self.client.post("/api/articles/{}/dislike/".format(self.slug))
        self.assertEqual(self.first_like_response.json(), self.first_dislike)

        # Let username_two like the article he previously disliked
        self.second_like_response = self.client.post("/api/articles/{}/like/".format(self.slug))
        self.assertEqual(self.second_like_response.json(), self.dislike_to_like)

        token = self.login_third.data['token']
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        self.third_like_response = self.client.post("/api/articles/{}/like/".format(self.slug))
        self.assertEqual(self.third_like_response.json(), self.first_like)

        # let username_three re-like this article
        token = self.login_third.data['token']
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        self.third_like_response = self.client.post("/api/articles/{}/like/".format(self.slug))
        self.assertEqual(self.third_like_response.json(), self.re_like)

        # Let username_three try to like an article that does not exist
        token = self.login_third.data['token']
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        self.third_like_response = self.client.post("/api/articles/404/like/")
        self.assertEqual(self.third_like_response.json(), self.article_404)













