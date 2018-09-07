from django.urls import path

from .views import (
    LoginAPIView, RegistrationAPIView, UserRetrieveUpdateAPIView, InvokePasswordResetAPIView 
)

urlpatterns = [
    path('user/', UserRetrieveUpdateAPIView.as_view()),
    path('users/', RegistrationAPIView.as_view()),
    path('users/login/', LoginAPIView.as_view()),
    path('users/reset/password', InvokePasswordResetAPIView.as_view()),
    path('user/reset-password/<token>', UserRetrieveUpdateAPIView.as_view())
]
