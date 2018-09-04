from django.urls import path

from authors.apps.social_auth.views import (
    GoogleSocialAuthView, FacebookSocialAuthView
)

urlpatterns = [
    path('auth/google/', GoogleSocialAuthView.as_view()),
    path('auth/facebook/', FacebookSocialAuthView.as_view()),
]
