"""
Serializer classes for articles
"""

from rest_framework.pagination import PageNumberPagination
from .serializers_extra import *


class PaginatedArticleSerializer(PageNumberPagination):
    """
    Pagination class
    Inherits from PageNumberPagination
    Paginates articles
    """
    page_size = 4

    def get_paginated_response(self, data):
        """
        Formats response to include page links
        :param data:
        :return:
        """
        return {
            'links': {
                'next': self.get_next_link(),
                'previous': self.get_previous_link()
            },
            'count': self.page.paginator.count,
            'results': data
        }


class RatingSerializer(serializers.ModelSerializer):
    """
    Define action logic for an article rating
    """
    article = serializers.PrimaryKeyRelatedField(
        queryset=Article.objects.all())
    rated_at = serializers.DateTimeField(read_only=True)
    rated_by = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    score = serializers.DecimalField(
        required=True, max_digits=4, decimal_places=2)

    @staticmethod
    def update_request_data(data, slug, user: User):
        """
        :param user:
        :param slug:
        :param data:
        :return:
        """
        try:
            article = Article.objects.get(slug__exact=slug)
        except Article.DoesNotExist:
            raise NotFoundException("Article is not found.")

        if article.author == user:
            raise serializers.ValidationError({
                "article": ["You can not rate your self"]
            })

        score = data.get("score", 0)
        if score > 5 or score < 0:
            raise serializers.ValidationError({
                "score": ["Score value must not go below `0` and not go beyond `5`"]
            })

        data.update({"article": article.pk})
        data.update({"rated_by": user.pk})
        return data

    def create(self, validated_data):
        """
        :param validated_data:
        :return:
        """
        rated_by = validated_data.get("rated_by", None)
        article = validated_data.get("article", None)
        score = validated_data.get("score", 0)

        try:
            rating = Rating.objects.get(
                rated_by=rated_by, article__slug=article.slug)
        except Rating.DoesNotExist:
            return Rating.objects.create(**validated_data)

        rating.score = score
        rating.save()
        return rating

    def to_representation(self, instance):
        """
        :param instance:
        :return:
        """
        response = super().to_representation(instance)

        response['article'] = instance.article.slug
        response['rated_by'] = instance.rated_by.username
        response['average_rating'] = instance.article.average_rating
        return response

    class Meta:
        """
        class behaviours
        """
        model = Rating
        fields = ("score", "rated_by", "rated_at", "article")


class ArticleReportSerializer(serializers.ModelSerializer):
    """
    Handles serialization and deserialization of ArticleReportSerializer objects.
    """

    def create(self, validated_data):
        return ArticleReport.objects.create(**validated_data)

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response["user"] = instance.user.username
        response["article"] = instance.article.slug
        return response

    class Meta:
        model = ArticleReport
        fields = ['user', 'article', 'report_message']