from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from authors.apps.social_auth.common import BaseClassAttributes
from authors.apps.social_auth.serializers import GoogleSocialAuthViewSerializer, FacebookSocialAuthViewSerializer


class GoogleSocialAuthView(APIView, BaseClassAttributes):
    serializer_class = GoogleSocialAuthViewSerializer

    def post(self, request):
        return HandleRequest.handle_user(request, self.serializer_class)


class FacebookSocialAuthView(APIView, BaseClassAttributes):
    serializer_class = FacebookSocialAuthViewSerializer

    def post(self, request):
        return HandleRequest.handle_user(request, self.serializer_class)


class HandleRequest:

    @classmethod
    def handle_user(cls, request, serializer_class):
        user = request.data.get('user', {})

        # Notice here that we do not call `serializer.save()` like we did for
        # the registration endpoint. This is because we don't actually have
        # anything to save. Instead, the `validate` method on our serializer
        # handles everything we need.
        serializer = serializer_class(data=user)
        serializer.is_valid(raise_exception=True)

        return Response(serializer.data, status=status.HTTP_200_OK)
