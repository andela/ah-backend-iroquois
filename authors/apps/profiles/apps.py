from django.apps import AppConfig


class MyAppConfig(AppConfig):
    name = 'authors.apps.profiles'

    def ready(self):
        import authors.apps.profiles.signals

