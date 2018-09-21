"""
Defines urls used in article package
"""
from django.urls import path
from rest_framework.routers import DefaultRouter

from authors.apps.articles.views import (FavoriteArticlesAPIView,
                                         ArticleViewSet, TagViewSet, RatingsView, ArticleReportView,
                                         CommentsView, RepliesView)

urlpatterns = [

    path('<article_slug>/favorite/',
         FavoriteArticlesAPIView.as_view(), name="favorite"),
    path('<article_slug>/unfavorite/',
         FavoriteArticlesAPIView.as_view(), name="unfavorite"),
    path("<slug>/rate/", RatingsView.as_view()),
    path('<slug>/comment/', CommentsView.as_view()),
    path('comment/<Id>/', CommentsView.as_view()),
    path('comment/', CommentsView.as_view()),
    path('comment/<commentID>/replies/', RepliesView.as_view()),
    path('comment/replies/<Id>/', RepliesView.as_view()),

    path("<slug>/rate/", RatingsView.as_view()),
    path("reports/", ArticleReportView.as_view()),
    path("reports/<slug>/", ArticleReportView.as_view()),
]

router = DefaultRouter()
router.register(r"", ArticleViewSet, base_name="article")
router.register(r"tags/tag_list", TagViewSet, base_name="tag_list")

urlpatterns += router.urls
