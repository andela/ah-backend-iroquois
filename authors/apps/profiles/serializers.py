from rest_framework import serializers

from authors.apps.profiles.models import UserProfile


class RetrieveUserProfileSerializer(serializers.ModelSerializer):

    username = serializers.CharField(source='user.username')
    bio = serializers.CharField(allow_blank=True, required=False)
    first_name = serializers.CharField(allow_blank=True, required=False)
    last_name = serializers.CharField(allow_blank=True, required=False)
    location = serializers.CharField(allow_blank=True, required='False')

    class Meta:
        model = UserProfile
        fields = ('username', 'bio', 'first_name', 'last_name', 'location')
        read_only_fields = ('username',)
        extra_kwargs = {'token': {'read_only': True}}
