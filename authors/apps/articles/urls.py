"""
Defines urls used in article package
"""
from django.urls import path
from rest_framework.routers import DefaultRouter

from authors.apps.articles.views import ArticleViewSet, RatingsView

urlpatterns = [
    path("<slug>/rate/", RatingsView.as_view())
]

router = DefaultRouter()
router.register(r"", ArticleViewSet, base_name="article")

urlpatterns += router.urls
