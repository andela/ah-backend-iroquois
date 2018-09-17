from rest_framework import serializers

from authors.apps.profiles.models import UserProfile


class UserProfileSerializer(serializers.ModelSerializer):

    username = serializers.CharField(source='user.username')
    following = serializers.SerializerMethodField()
    followers = serializers.SerializerMethodField()

    class Meta:
        model = UserProfile
        fields = ('username', 'bio', 'first_name', 'last_name', 'location', 'avatar', 'following', 'followers')
        read_only_fields = ('username',)
        extra_kwargs = {'token': {'read_only': True}}

    def helper(self, field):
        request = self.context.get('request', None)
        if field == 'following':
            profiles = request.user.userprofile.following.all()
        elif field == 'followers':
            profiles = request.user.userprofile.followers.all()
        return [profile.user.username for profile in profiles]

    def get_following(self, instance):
        return self.helper('following')

    def get_followers(self, instance):
        return self.helper('followers')
