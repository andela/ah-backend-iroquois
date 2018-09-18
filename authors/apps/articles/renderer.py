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
        val = data.get("results", None)
        if val and isinstance(val, list) and len(val) > 1:
            return json.dumps({
                'articles': data
            })

        if val and isinstance(val, list) and len(val) is 1:
            val = val[0]

        if val is not None:
            data.update({"results": val})

        errors = data.get('errors', None)

        if errors is not None:
            return super(ArticleJSONRenderer, self).render(data)

        return json.dumps({
            'article': data
        })
