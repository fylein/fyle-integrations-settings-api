from django.apps import AppConfig


class BamboohrConfig(AppConfig):
    name = 'apps.bamboohr'

    def ready(self):
        super(BamboohrConfig, self).ready()
        import apps.bamboohr.signals
