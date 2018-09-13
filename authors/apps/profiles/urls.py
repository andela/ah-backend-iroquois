from django.urls import path
from .views import (
    RetrieveUserProfileAPIView, UpdateUserProfileAPIView
)

urlpatterns = [
    path('profile/<username>/', RetrieveUserProfileAPIView.as_view(), name="view_profile"),
    path('user/update/profile/', UpdateUserProfileAPIView.as_view(), name="update_profile"),

]
