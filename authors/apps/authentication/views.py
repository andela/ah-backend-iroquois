from rest_framework import status
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .renderers import UserJSONRenderer
from .serializers import (
    LoginSerializer, RegistrationSerializer, UserSerializer, InvokePasswordReset
)
import os
from .utils import send_password_reset_email


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

        return Response(serializer.data, status=status.HTTP_201_CREATED)


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

    def update(self, request, *args, **kwargs):
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
        send_password_reset_email(user['email'], serializer.data['email'], current_site)

        return Response({"message": "Check your email for a link"}, status=status.HTTP_200_OK)



    

