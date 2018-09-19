"""
Defines urls used in article package
"""
from django.urls import path
from rest_framework.routers import DefaultRouter

from authors.apps.articles.views import ArticleViewSet, FavoriteArticlesAPIView, TagViewSet, RatingsView

urlpatterns = [
    path('<article_slug>/favorite/', FavoriteArticlesAPIView.as_view(), name="favorite"),
    path('<article_slug>/unfavorite/', FavoriteArticlesAPIView.as_view(), name="unfavorite"),
    path("<slug>/rate/", RatingsView.as_view()),
]

router = DefaultRouter()
router.register(r"", ArticleViewSet, base_name="article")
router.register(r"tags/tag_list", TagViewSet, base_name="tag_list")

urlpatterns += router.urls
