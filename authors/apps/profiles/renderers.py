
import json
from datetime import datetime

from django.conf.global_settings import DATETIME_FORMAT
from rest_framework.renderers import JSONRenderer


class AHJSONRenderer(JSONRenderer):
    charset = 'utf-8'
    object_label = 'object'

    def render(self, data, media_type=None, renderer_context=None):

        return json.dumps({
            self.object_label: data
        })


class ProfileJSONRenderer(AHJSONRenderer):
    object_label = 'profile'
