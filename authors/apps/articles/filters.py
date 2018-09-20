"""
Implements article search and filter
"""
from urllib.parse import unquote

from django.db import models
from django.db.models import Q

from authors.apps.articles.filter_search_extras import extra_vars, get_response


class ArticleManager(models.Manager):
    """
    define custom manager for articles
    """

    def search(self, params):
        """
        customised search functionality
        """
        author = unquote(params.get("author", ""))
        title = unquote(params.get("title", ""))
        tag = unquote(params.get("tag", ""))

        author_query = (Q(author__username__icontains=author) | Q(author__email__exact=author))
        tag_query = Q(tags__tag_name__exact=tag)
        title_query = Q(title__icontains=title)

        all_fields = (author and title and tag)
        author_and_title = (author and title and not tag)
        author_and_tag = (author and tag and not title)
        author_only, tag_only, title_and_tag, title_only = extra_vars(all_fields, author, tag, title)

        queryset = self.get_queryset()

        attrs = (all_fields, author_and_tag, author_and_title, author_only, queryset, tag_only,
                 title_and_tag, title_only, author_query, title_query, tag_query)

        return get_response(attrs)
