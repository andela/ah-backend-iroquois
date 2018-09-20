from rest_framework.response import Response
from authors.apps.articles.exceptions import NotFoundException
from .models import Article


def return_article(slug):
    """ This method returns the article with the provided slug """
    try:
        article = Article.objects.get(slug__exact=slug)
        return article
    except Article.DoesNotExist:
        raise NotFoundException("Article is not found.")


def make_first_preference_attempt(action, slug, current_user):
    """ Called when user is liking or disliking for the first time """

    article = return_article(slug)
    if action == "like":
        article.like(current_user)
        article.save()
        message = {"message": "You like this article"}
        return Response(message)
    article.dislike(current_user)
    article.save()
    return Response({"message": "You dislike this article"})


def change_preference(action, slug, current_user):
    """ This method is called when user wants to make a change to the preference"""

    article = return_article(slug)

    if action == "like":

        # User likes the article
        if article.is_disliking(current_user):
            article.dislike_to_like(current_user)
            return Response({"message": "You now like this article"})

        # current user is re liking
        article.un_like(current_user)
        return Response({"message": "You no longer like this article"})

    # action is a dislike
    if article.is_liking(current_user):
        article.like_to_dislike(current_user)
        return Response({"message": "You now dislike this article"})

    # current user is re disliking
    article.un_dislike(current_user)
    return Response({"message": "You no longer dislike this article"})


def call_preference_helpers(action, slug, current_user):
    """ Called with in the post methods to call other helper function
        To like, unlike, dislike and un_dislike an article
    """

    article = return_article(slug)
    if article.is_neutral(current_user):
        return make_first_preference_attempt(action, slug, current_user)
    return change_preference(action, slug, current_user)

