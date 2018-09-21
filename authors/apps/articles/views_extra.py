from django.http import Http404
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from authors.apps.articles.exceptions import NotFoundException
from authors.apps.articles.models import Comments, Article, Replies
from authors.apps.articles.serializers import RepliesSerializer, CommentSerializer


def get_object(obj_Class, pk):
    try:
        return obj_Class.objects.get(pk=pk)
    except obj_Class.DoesNotExist:
        raise Http404


class CommentsView(APIView):

    permission_classes = (IsAuthenticated,)

    def post(self, request, slug):
        """
        :param request:
        :param slug:
        :return:
        """

        content_data = request.data.get('comment',None)
        try:
            instance = Article.objects.get(slug=slug)
            author = request.user
            content_data['article'] = instance.id
            content_data['author'] = author.id
            serializer = CommentSerializer(data=content_data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            print('serializer data', serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Article.DoesNotExist:
            return Response({"message": "Sorry, this article is not found."}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, Id):
        """
        :param request:
        :param Id:
        :return:
        """
        snippet = get_object(Comments, Id)
        content_data = request.data.get('comment',None)
        content_data['author'] = request.user.id
        serializer = CommentSerializer(snippet, data=content_data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, instance,  Id):
        """
        :param instance:
        :param Id:
        :return:
        """

        try:
            instance = Comments.objects.get(id=Id,)
            if str(instance):
                instance.delete()
        except Comments.DoesNotExist:
            raise NotFoundException("Comment  is not found for delete.")
        return Response({"message", "Comment deleted successfully"}, status=status.HTTP_204_NO_CONTENT)


class RepliesView(APIView):

    permission_classes = (IsAuthenticated,)

    def post(self, request, commentID):
        """
        :param request:
        :param commentID:
        :return:
        """

        try:
            content_data = request.data.get('reply',None)
            author = request.user
            instance = Comments.objects.get(id=commentID)
            content_data['author'] = author.id
            content_data['comment'] = instance.id
            serializer = RepliesSerializer(data=content_data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Comments.DoesNotExist:
            return Response({"message": "Sorry, this comment is not found."}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, Id, format=None):
        """
        :param request:
        :param Id:
        :param format:
        :return:
        """
        snippet = get_object(Replies, Id)
        snippet.delete()
        return Response({"message": "Reply Deleted Successfully."}, status=status.HTTP_204_NO_CONTENT)

    def put(self, request, Id):
        """
        :param request:
        :param Id:
        :return:
        """
        content = get_object(Replies, Id)
        serializer = RepliesSerializer(content, data=request.data.get('reply', None))
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)