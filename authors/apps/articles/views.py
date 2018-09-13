"""
Views for articles
"""
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from authors.apps.articles.exceptions import NotFoundException, InvalidQueryParameterException
from authors.apps.articles.models import Article
from authors.apps.articles.renderer import ArticleJSONRenderer
from authors.apps.articles.serializers import ArticleSerializer


# noinspection PyUnusedLocal,PyMethodMayBeStatic
class ArticleViewSet(ViewSet):
    """
    Article ViewSet
    Handles all request methods
    Post, Get, Put, Delete
    """
    permission_classes = (IsAuthenticated,)
    renderer_classes = (ArticleJSONRenderer,)
    serializer_class = ArticleSerializer
    lookup_field = "slug"

    def list(self, request):
        """
        returns a list of all articles
        :param request:
        :return:
        """
        author = request.query_params.get("author", None)
        limit = request.query_params.get("limit", 20)
        offset = request.query_params.get("offset", 0)

        def to_int(val):
            """
            convert param to positive integer
            :param val:
            :return:
            """
            return int(val) if int(val) > 0 else -int(val)

        try:
            limit = to_int(limit)
            offset = to_int(offset)
        except ValueError:
            raise InvalidQueryParameterException()

        queryset = Article.objects.all()
        if queryset.count() > 0:
            queryset = queryset[offset:limit]

        serializer = self.serializer_class(queryset, many=True)
        data = serializer.data

        return Response(data)

    def retrieve(self, request, slug=None):
        """
        returns a specific article based on primary key
        :param slug:
        :param request:
        :return:
        """
        queryset = Article.objects.all()
        article = get_object_or_404(queryset, slug=slug)
        serializer = self.serializer_class(article)
        return Response(serializer.data)

    def create(self, request):
        """
        creates an article
        :param request:
        :return:
        """
        article = request.data.get("article", {})
        article.update({"author": request.user.pk})

        serializer = self.serializer_class(data=article)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, slug=None):
        """
        update a specific article
        :param request:
        :param slug:
        :return:
        """
        article_update = request.data.get("article", {})

        article, article_update = self.serializer_class.validate_for_update(
            article_update, request.user, slug)

        serializer = self.serializer_class(data=article_update)
        serializer.instance = article
        serializer.is_valid(raise_exception=True)

        serializer.update(article, serializer.validated_data)

        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)

    def destroy(self, request, slug=None):
        """
        delete an article
        :param request:
        :param slug:
        :return:
        """

        try:
            article = Article.objects.filter(slug__exact=slug, author__exact=request.user)
            if article.count() > 0:
                article = article[0]
            else:
                raise Article.DoesNotExist

            article.delete()
        except Article.DoesNotExist:
            raise NotFoundException("Article is not found for update.")

        return Response({"detail": "Article has been deleted."}, status=status.HTTP_204_NO_CONTENT)
