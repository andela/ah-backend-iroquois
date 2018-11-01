from rest_framework import serializers

from authors.apps.articles.models import Article
from authors.apps.profiles.models import UserProfile


class UserProfileSerializer(serializers.ModelSerializer):

    username = serializers.CharField(source='user.username')
    following = serializers.SerializerMethodField()
    followers = serializers.SerializerMethodField()
    favorites = serializers.SerializerMethodField()

    class Meta:
        model = UserProfile
        fields = ('username', 'bio', 'first_name', 'last_name', 'location', 'avatar', 'following', 'followers',
                  'favorites')
        read_only_fields = ('username',)
        extra_kwargs = {'token': {'read_only': True}}

    def helper(self, field, instance=None):
        request = self.context.get('request', None)
        if field == 'favorites':
            favorites = instance.favorites.through.objects.filter(userprofile__user=instance.user)

            return [Article.objects.get(pk=favorite.article_id).slug for favorite in favorites]

        if field == 'following':
            profiles = instance.following.all()
        elif field == 'followers':
            profiles = instance.followers.all()
        return [profile.user.username for profile in profiles]

    def get_following(self, instance):
        return self.helper('following', instance)

    def get_followers(self, instance):
        return self.helper('followers', instance)

    def get_favorites(self, instance):
        return self.helper('favorites', instance)
