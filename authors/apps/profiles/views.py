from rest_framework.exceptions import NotFound
from rest_framework.generics import RetrieveUpdateAPIView, RetrieveAPIView
from rest_framework import status, serializers
from rest_framework.views import APIView

from authors.apps.profiles.models import UserProfile
from rest_framework.permissions import IsAuthenticated
from .serializers import UserProfileSerializer
from .exceptions import UserProfileDoesNotExist
from rest_framework.response import Response
from .renderers import ProfileJSONRenderer


class UserProfileAPIView(RetrieveUpdateAPIView):
    """ This class retrieve information about the user
        Is accessible to anonymous users

    """
    permission_classes = (IsAuthenticated,)
    renderer_classes = (ProfileJSONRenderer,)
    serializer_class = UserProfileSerializer

    def retrieve(self, request, username, *args, **kwargs):

        """ Function retrieves profile for the user with provided username """
        try:

            queryset = UserProfile.objects.get(
                user__username=username
            )

        except UserProfile.DoesNotExist:
            raise UserProfileDoesNotExist

        serializer = self.serializer_class(instance=queryset, context={'request': request})

        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        """ Function to update user information """

        user_data = request.data.get('profile', {})

        serializer_data = {
            'username': user_data.get('username', request.user.username),
            'email': user_data.get('email', request.user.email),
            'bio': user_data.get('bio', request.user.userprofile.bio),
            'first_name': user_data.get('first_name', request.user.userprofile.first_name),
            'last_name': user_data.get('last_name', request.user.userprofile.last_name),
            'location': user_data.get('location', request.user.userprofile.location),
            'avatar': user_data.get('avatar', request.user.userprofile.avatar)
        }

        serializer = self.serializer_class(
            request.user.userprofile, data=serializer_data, context={'request': request}, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.update(request.user.userprofile, serializer_data)

        try:
            serializer.update(request.user, serializer_data)
        except:
            return Response({"error": "Username or email already exist, recheck and try again"}, status.HTTP_400_BAD_REQUEST)

        return Response(serializer.data, status=status.HTTP_200_OK)


class FollowUnfollowUserAPIView(APIView):

    permission_classes = (IsAuthenticated,)
    serializer_class = UserProfileSerializer

    def post(self, request, username=None):
        current_user = self.request.user

        try:
            follow = UserProfile.objects.get(user__username=username)
        except UserProfile.DoesNotExist:
            raise NotFound('Profile with this username was not found.')

        if follow.pk is current_user.pk:
            raise serializers.ValidationError('You cannot follow yourself.')

        current_user_profile = UserProfile.objects.get(user=current_user)

        if current_user_profile.is_following(follow):
            return Response({"message": "You are already following that user"}, status=status.HTTP_400_BAD_REQUEST)

        current_user_profile.follow(follow)
        current_user_profile.save()

        serializer = self.serializer_class(current_user_profile, context={'request': request})

        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, username=None):
        current_user = self.request.user

        try:
            unfollow = UserProfile.objects.get(user__username=username)
        except UserProfile.DoesNotExist:
            raise NotFound('Profile with this username was not found.')

        current_user_profile = UserProfile.objects.get(user=current_user)

        if not current_user_profile.is_following(unfollow):
            return Response({"message": "You cannot un-follow a user you do not follow"},
                            status=status.HTTP_400_BAD_REQUEST)

        current_user_profile.unfollow(unfollow)
        current_user_profile.save()
        serializer = self.serializer_class(current_user_profile, context={'request': request})

        return Response(serializer.data, status=status.HTTP_200_OK)
