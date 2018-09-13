from rest_framework.generics import RetrieveUpdateAPIView, RetrieveAPIView
from rest_framework import status
from authors.apps.profiles.models import UserProfile
from rest_framework.permissions import IsAuthenticated
from .serializers import RetrieveUserProfileSerializer
from .exceptions import UserProfileDoesNotExist
from rest_framework.response import Response
from .renderers import ProfileJSONRenderer


class RetrieveUserProfileAPIView(RetrieveUpdateAPIView):
    """ This class retrieve information about the user
        Is accessible to anonymous users

    """
    permission_classes = (IsAuthenticated,)
    renderer_classes = (ProfileJSONRenderer,)
    serializer_class = RetrieveUserProfileSerializer

    def retrieve(self, request, username, *args, **kwargs):

        """ Function retrieves profile for the user with provided username """
        try:

            queryset = UserProfile.objects.get(
                user__username=username
            )

        except UserProfile.DoesNotExist:
            raise UserProfileDoesNotExist

        serializer = self.serializer_class(instance=queryset)

        return Response(serializer.data, status=status.HTTP_200_OK)


class UpdateUserProfileAPIView(RetrieveUpdateAPIView):
    """ This class retrieve information about the user
        Is accessible to anonymous users

    """
    permission_classes = (IsAuthenticated,)
    renderer_classes = (ProfileJSONRenderer,)
    serializer_class = RetrieveUserProfileSerializer

    def update(self, request, *args, **kwargs):
        """ funtion to update user information """

        user_data = request.data.get('profile', {})

        serializer_data = {
            'username': user_data.get('username', request.user.username),
            'email': user_data.get('email', request.user.email),
            'bio': user_data.get('bio', request.user.userprofile.bio),
            'first_name': user_data.get('first_name', request.user.userprofile.first_name),
            'last_name': user_data.get('last_name', request.user.userprofile.last_name),
            'location': user_data.get('location', request.user.userprofile.location)
        }

        serializer = self.serializer_class(
            request.user.userprofile, data=serializer_data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.update(request.user.userprofile, serializer_data)

        try:
            serializer.update(request.user, serializer_data)
        except:
            return Response({"error": "Username or email already exist, recheck and try again"}, status.HTTP_400_BAD_REQUEST)

        return Response(serializer.data, status=status.HTTP_200_OK)
