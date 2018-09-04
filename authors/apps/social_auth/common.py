from django.contrib.auth import authenticate
from rest_framework import serializers
from rest_framework.permissions import AllowAny

from authors.apps.authentication.models import User
from authors.apps.authentication.renderers import UserJSONRenderer


def create_user_and_return_token(user_id, email, name):
    # check if the user id from decoded token exists in the decoded token dict
    user = User.objects.filter(social_id=user_id)

    # if user does not exist, register the user into the database.
    # i.e. create a new user
    if not user.exists():
        user = {
            'username': name, 'email': email, 'password': 'nopassword'}

        # create a new facebook user
        try:
            User.objects.create_user(**user)
        except:  # noqa: E722
            msg = 'User with email {0} already exists.'.format(email)
            raise serializers.ValidationError(
                msg
            )
        User.objects.filter(email=email).update(social_id=user_id)

        auth = authenticate(email=email, password="nopassword")
        return {
            auth.token
        }
    else:
        # if user already exists and is authenticated by google also,
        # return the user an authentication token
        auth = authenticate(email=email, password="nopassword")
        return auth.token


class BaseClassAttributes:
    permission_classes = (AllowAny,)
    renderer_classes = (UserJSONRenderer,)
