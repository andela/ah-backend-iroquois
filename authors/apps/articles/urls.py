"""
Defines urls used in article package
"""

from rest_framework.routers import DefaultRouter

from authors.apps.articles.views import ArticleViewSet

urlpatterns = []

router = DefaultRouter()
router.register(r"", ArticleViewSet, base_name="article")

urlpatterns += router.urls
