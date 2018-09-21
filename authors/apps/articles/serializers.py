"""
Serializer classes for articles
"""
from rest_framework import serializers
from rest_framework.pagination import PageNumberPagination
from authors.apps.articles.exceptions import NotFoundException

from authors.apps.articles.models import (Article,
                                          Tag, Rating, ArticleReport, Comments, Replies)
from authors.apps.articles.utils import get_date
from authors.apps.authentication.models import User
from authors.apps.profiles.models import UserProfile
from authors.apps.profiles.serializers import UserProfileSerializer
from rest_framework.exceptions import NotFound


class TagRelatedField(serializers.RelatedField):
    """
    Implements a custom relational field by overriding RelatedFied.
    returns a list of tag names.
    """

    def to_representation(self, value):

        return value.tag_name


class TagSerializer(serializers.ModelSerializer):
    """Handles serialization and deserialization of Tag objects."""

    class Meta:
        model = Tag
        fields = "__all__"


class RepliesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Replies
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):

    replies = RepliesSerializer(many=True, read_only=True)

    class Meta:
        model = Comments
        fields = ('id', 'body', 'article', 'author', 'replies')


class ArticleSerializer(serializers.ModelSerializer):
    """
    Define action logic for an article
    """
    user_rating = serializers.CharField(
        source='author.average_rating', required=False)
    tagList = TagRelatedField(
        many=True, required=False, source='tags', queryset=Tag.objects.all())
    author = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), required=False)
    slug = serializers.CharField(read_only=True)
    favorites_count = serializers.SerializerMethodField()
    tags = []
    comments = CommentSerializer(many=True, read_only=True)

    def create(self, validated_data):
        """
        :param validated_data:
        :return:
        """
        article = Article.objects.create(**validated_data)

        for tag in self.tags:
            article.tags.add(Tag.objects.get_or_create(
                tag_name=tag.replace(" ", "_").lower())[0])
        return article

    def update(self, instance, validated_data):
        """
        :param validated_data:
        :return:
        """
        for key, val in validated_data.items():
            setattr(instance, key, val)

        for tag in instance.tags.all():
            instance.tags.remove(tag)

        for tag in self.tags:
            instance.tags.add(Tag.objects.get_or_create(
                tag_name=tag.replace(" ", "_").lower())[0])
        instance.save()
        return instance

    @staticmethod
    def validate_for_update(data: dict, user, slug):
        """
        :param data:
        :param user:
        :param slug:
        :return:
        """
        try:
            article = Article.objects.filter(
                slug__exact=slug, author__exact=user)
            if article.count() > 0:
                article = article[0]
            else:
                raise Article.DoesNotExist

        except Article.DoesNotExist:
            raise NotFoundException("Article is not found for update.")

        required = {"title", "description", "body"}
        keys = set(data.keys())

        missing = required.difference(keys)

        for val in missing:
            data.update({val: article.__getattribute__(val)})

        data.update({
            "author": user.pk,
            "updated_at": get_date()
        })
        return article, data

    @staticmethod
    def get_article_object(slug):
        """This method returns an instance of Article"""
        article = None
        try:
            article = Article.objects.get(slug=slug)
        except Article.DoesNotExist:
            raise NotFound("An article with this slug does not exist")
        return article

    def to_representation(self, instance):
        """
        formats serializer display response
        :param instance:
        :return:
        """
        response = super().to_representation(instance)
        profile = UserProfileSerializer(UserProfile.objects.get(
            user=instance.author), context=self.context).data

        response['author'] = profile
        return response

    class Meta:
        """
        class behaviours
        """
        model = Article

        fields = ('slug', 'title', 'description', 'body', 'created_at', 'average_rating', 'user_rating',
                  'updated_at', 'favorites_count', 'photo_url', 'author', 'tagList', 'comments')

    def get_favorites_count(self, instance):
        return instance.favorited_by.count()


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
