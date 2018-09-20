"""
Define extra methods to handle extra work for
making search functionality
"""


def get_response(attrs):
    """
    :param attrs:
    :return:
    """
    all_fields, author_and_tag, author_and_title, author_only, queryset, tag_only, \
    title_and_tag, title_only, author_query, title_query, tag_query = attrs

    boolean_mapping = {
        "all_fields": all_fields,
        "author_and_tag": author_and_tag,
        "author_and_title": author_and_title,
        "title_and_tag": title_and_tag,
        "author_only": author_only,
        "title_only": title_only,
        "tag_only": tag_only,
    }
    function_mapping = {
        "all_fields": lambda: queryset.filter(author_query & title_query & tag_query),
        "author_and_tag": lambda: queryset.filter(author_query & tag_query),
        "author_and_title": lambda: queryset.filter(author_query & title_query),
        "title_and_tag": lambda: queryset.filter(title_query & tag_query),
        "author_only": lambda: queryset.filter(author_query),
        "title_only": lambda: queryset.filter(title_query),
        "tag_only": lambda: queryset.filter(tag_query),
    }
    for key, val in boolean_mapping.items():
        if val:
            return function_mapping.get(key)()
    return queryset.all()


def extra_vars(all_fields, author, tag, title):
    """
    :param all_fields:
    :param author:
    :param tag:
    :param title:
    :return:
    """
    title_and_tag = (title and tag and not author)
    author_only = (author and not all_fields)
    title_only = (title and not author and not tag)
    tag_only = (tag and not title and not author)

    return author_only, tag_only, title_and_tag, title_only
