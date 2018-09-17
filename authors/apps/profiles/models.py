from django.db import models
from authors.apps.authentication.models import User


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True, null=True)
    avatar = models.URLField(blank=True, null=True)
    first_name = models.CharField(max_length=50, blank=True, null=True)
    last_name = models.CharField(max_length=50, blank=True, null=True)

    # A timestamp representing when this object was created.
    created_at = models.DateTimeField(auto_now_add=True)
    birth_date = models.DateField(null=True, blank=True)
    location = models.CharField(max_length=100, null=True, blank=True)

    # A timestamp representing when this object was last updated.
    updated_at = models.DateTimeField(auto_now=True)

    following = models.ManyToManyField('self', related_name='followers', symmetrical=False)

    def __str__(self):
        return self.user.username

    def follow(self, profile):
        """Following a user"""
        self.following.add(profile)

    def unfollow(self, profile):
        """Unfollow a user"""
        self.following.remove(profile)

    def is_following(self, profile):
        """To check if a user is already following the profile"""
        return self.following.filter(pk=profile.pk).exists()
