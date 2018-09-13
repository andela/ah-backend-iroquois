from django.core.mail import send_mail
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from rest_framework import status
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from authors.apps.authentication.backends import JWTAuthentication
from authors.apps.authentication.models import User
from authors.apps.authentication.utils import send_password_reset_email
from .renderers import UserJSONRenderer
from .serializers import (
    LoginSerializer, RegistrationSerializer, UserSerializer,
    InvokePasswordReset, UsersListSerializer)


class RegistrationAPIView(APIView):
    # Allow any user (authenticated or not) to hit this endpoint.
    permission_classes = (AllowAny,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = RegistrationSerializer

    def post(self, request):
        user = request.data.get('user', {})

        # The create serializer, validate serializer, save serializer pattern
        # below is common and you will see it a lot throughout this course and
        # your own work later on. Get familiar with it.
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user_data = serializer.data
        uid = force_text(urlsafe_base64_encode(user['email'].encode("utf8")))
        # Send a user a verification email on successful register.
        send_mail(
            'Authors Haven account activation.',
            'Hey there, Thank you for expressing interest in Authors Haven. '
            'Follow the link to activate your account {}/api/users/activate_account/{}/{}/'
            .format(request.get_host(), uid, user_data['token']),
            'no-reply@uio.nm',
            [user['email']],
            fail_silently=False,
        )
        user_data.update({
            'message': 'A verification link has been sent by mail.',
            'link': '{}/api/users/activate_account/{}/{}/'.format(request.get_host(), uid, user_data['token'])
        })
        del user_data['token']

        return Response(user_data, status=status.HTTP_201_CREATED)


class LoginAPIView(APIView):
    permission_classes = (AllowAny,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = LoginSerializer

    def post(self, request):
        user = request.data.get('user', {})

        # Notice here that we do not call `serializer.save()` like we did for
        # the registration endpoint. This is because we don't actually have
        # anything to save. Instead, the `validate` method on our serializer
        # handles everything we need.
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserRetrieveUpdateAPIView(RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticated,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = UserSerializer

    def retrieve(self, request, *args, **kwargs):
        # There is nothing to validate or save here. Instead, we just want the
        # serializer to handle turning our `User` object into something that
        # can be JSONified and sent to t he client.
        serializer = self.serializer_class(request.user)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, pk=None, **kwargs):
        serializer_data = request.data.get('user', {})

        # Here is that serialize, validate, save pattern we talked about
        # before.
        serializer = self.serializer_class(
            request.user, data=serializer_data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)


class InvokePasswordResetAPIView(LoginAPIView):
    """ 
        This view allows the user to invoke a password reset email
        It inherits post method of the LoginAPIView
    """
    permission_classes = (AllowAny,)
    serializer_class = InvokePasswordReset

    def post(self, request):
        user = request.data.get('user', {})

        # get current site
        if 'HTTP_HOST' in request.META:
            current_site = request.META['HTTP_HOST']
            current_site = "https://{}".format(current_site)
        else:
            current_site = "http://127.0.0.1:8000"

        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)

        # call send email function
        send_password_reset_email(
            user['email'], serializer.data['email'], request.get_host())

        return Response({"message": "Check your email for a link"}, status=status.HTTP_200_OK)


class ActivateAccountView(APIView, JWTAuthentication):

    def get(self, request, uid, token):
        try:
            email = force_text(urlsafe_base64_decode(uid))
            user = User.objects.get(email=email)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist) as e:
            return Response({"error": str(e)})

        verified_user, verified_token = self.authenticate_credentials(
            request, token)

        if user and (verified_user.email == user.email) and not user.is_email_verified:
            user.is_active = True
            user.is_email_verified = True
            user.save()

            return Response({'message': 'Email verified, continue to login'}, status=status.HTTP_200_OK)
        if user and user.is_email_verified:
            return Response({'message': 'Email is already verified, continue to login'}, status=status.HTTP_200_OK)

        return Response({'error': 'Activation link invalid or expired.'}, status=status.HTTP_400_BAD_REQUEST)


class UsersListAPIView(RetrieveUpdateAPIView):
    """
    This class is responsible for the handling users with 
    their profiles.
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = UsersListSerializer

    def retrieve(self, request):
        """
        This method returns a list of users with their profiles.
        """
        queryset = User.objects.filter(is_active=True, is_email_verified=True)
        serializer = self.serializer_class(queryset, many=True)

        return Response({'users': serializer.data}, status=status.HTTP_200_OK)
