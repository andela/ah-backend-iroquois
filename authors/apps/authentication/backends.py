"""
This module decides whether a user is authenticated.
"""
import jwt

from django.conf import settings

from rest_framework import authentication, exceptions

from .models import User


class JWTAuthentication(authentication.BaseAuthentication):

    """
    This class implements a custom authentication by subclassing
    'BaseAuthentication' class and overriding '.authenticate(self, request)'
    method.
    """

    header_token = 'token'

    def authenticate(self, request):
        """
        This method returns None if no authentication is required and returns a turple
        containing a user and token if the authentication is required and successful.
        Else an error is returned.
        """
        request.user = None
        auth_header = authentication.get_authorization_header(request).split()

        if not auth_header:
            return None

        if len(auth_header) == 1:
            error_message = 'Incomplete authentication details provided'
            raise exceptions.NotAuthenticated(error_message)

        if len(auth_header) > 2:
            error_message = 'Excess authentication details provided'
            raise exceptions.NotAuthenticated(error_message)

        if auth_header[0].lower().decode('utf-8') != self.header_token:
            error_message = 'Unknown header prefix was provided.'
            raise exceptions.NotAuthenticated(error_message)

        return self.authenticate_credentials(request, auth_header[1].decode('utf-8'))

    def authenticate_credentials(self, request, token):
        """
        This method authenticates the credentials provided.
        :return: (user, token) or an error
        """
        try:
            payload = jwt.decode(token, settings.SECRET_KEY)

        except jwt.InvalidTokenError:
            error_message = 'Invalid token. Please log in again.'
            raise exceptions.AuthenticationFailed(error_message)

        try:
            user = User.objects.get(id=payload['id'])
        except User.DoesNotExist:
            error_message = 'No user matching this token was found.'
            raise exceptions.AuthenticationFailed(error_message)

        if not user.is_active:
            error_message = 'This user has been deactivated.'
            raise exceptions.AuthenticationFailed(error_message)

        return (user, token)
