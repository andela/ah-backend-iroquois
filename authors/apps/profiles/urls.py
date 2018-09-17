from django.urls import path
from .views import (UserProfileAPIView, FollowUnfollowUserAPIView
)

urlpatterns = [
    path('profile/<username>/', UserProfileAPIView.as_view(), name="view_profile"),
    path('user/update/profile/', UserProfileAPIView.as_view(), name="update_profile"),
    path('profile/<username>/follow', FollowUnfollowUserAPIView.as_view(), name="follow_user"),
    path('profile/<username>/unfollow', FollowUnfollowUserAPIView.as_view(), name="unfollow_user"),
]
