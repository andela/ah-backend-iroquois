"""
Renderer classes go here
"""
import json

from rest_framework.renderers import JSONRenderer


class ArticleJSONRenderer(JSONRenderer):
    """
    Override default renderer to customise output
    """
    charset = 'utf-8'

    def render(self, data, accepted_media_type=None, renderer_context=None):
        """
        render response data
        :param data:
        :param accepted_media_type:
        :param renderer_context:
        :return:
        """
        if isinstance(data, list) and len(data) > 1:
            return json.dumps({
                'articles': data
            })

        if isinstance(data, list) and len(data) is 1:
            data = data[0]

        if isinstance(data, list) and len(data) < 1:
            data = {}

        errors = data.get('errors', None)

        if errors is not None:
            return super(ArticleJSONRenderer, self).render(data)

        return json.dumps({
            'article': data
        })
