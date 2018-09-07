from rest_framework import serializers

from authors.apps.social_auth import google, facebook
from authors.apps.social_auth.common import create_user_and_return_token


# noinspection PyMethodMayBeStatic
class GoogleSocialAuthViewSerializer(serializers.Serializer):
    """ Handles all social auth related tasks from google """

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass

    # get google authentication token from and do validations
    auth_token = serializers.CharField()

    def validate_auth_token(self, auth_token) -> object:

        # create an instance of the google social auth lib and validate token
        user_info = google.GoogleAuth.validate(auth_token)

        try:
            user_info['sub']
        except:  # noqa: E722
            raise serializers.ValidationError(
                'The token is either invalid or expired. Please login again.'
            )
        user_id = user_info['sub']

        keys = user_info.keys()
        email = user_info['email'] if 'email' in user_info.keys() else user_info['name']
        name = "{0}_{1}".format(user_info['name'], user_id) if 'name' in keys else 'noname_{0}'.format(user_id)

        return create_user_and_return_token(user_id=user_id, email=email, name=name)


# noinspection PyMethodMayBeStatic
class FacebookSocialAuthViewSerializer(serializers.Serializer):
    """ Handles all social auth related tasks from google """

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass

    # get google authentication token from and do validations
    auth_token = serializers.CharField()

    def validate_auth_token(self, auth_token):

        # create an instance of the google social auth lib and validate token
        user_info = facebook.FacebookValidate.validate(auth_token)

        # check if facebook managed to decode token
        # this is by checking if key sub exists
        try:
            user_info['id']
        except:  # noqa: E722
            raise serializers.ValidationError(
                'The token is either invalid or expired. Please login again.'
            )

        user_id = user_info['id']
        keys = user_info.keys()

        email = "{0}_{1}".format(user_id, user_info['email']) if 'email' in keys else "{0}_no@email".format(user_id)

        name = "{0}_{1}".format(user_info['name'], user_id) if 'name' in keys else 'noname_{0}'.format(user_id)

        return create_user_and_return_token(user_id=user_id, email=email, name=name)
