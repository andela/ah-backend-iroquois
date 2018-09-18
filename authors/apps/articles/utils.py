"""
Utils file,
Define all necessary functions here
"""
import math
from collections import Counter
from datetime import datetime
from django.template.defaultfilters import slugify


def get_common_words(story, max_words=5):
    """
    return a list of common words in a statement or sentence
    :param story:
    :param max_words:
    :return:
    """
    split_it = story.split()
    counter = Counter(split_it)
    return dict(counter.most_common(max_words)).keys()


def create_unique_number():
    """
    returns a unique random number
    :return:
    """
    return datetime.now().strftime("%Y%m%d%H%M%S%f")


def get_date():
    """
    returns date in the format `yyyy-mm-dd HH:MM:SS`
    :return:
    """
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")


def generate_slug(cls, self):
    """
    returns a slug
    :param cls:
    :param self:
    :return:
    """
    if self.id:
        return self.slug

    temp_slug = slugify(self.title)
    if cls.objects.filter(slug=temp_slug).count() > 0:
        size = math.floor(len(self.description.split()) / 2)
        temp_slug = slugify(temp_slug + " " + " ".join(self.description.split()[:size]))

    if cls.objects.filter(slug=temp_slug).count() > 0:
        temp_slug = slugify(temp_slug + " " + " ".join(get_common_words(self.body, 10)))

    if cls.objects.filter(slug=temp_slug).count() > 0:
        temp_slug = slugify(temp_slug + "-" + create_unique_number())

    return temp_slug
