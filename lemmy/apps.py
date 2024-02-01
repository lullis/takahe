from django.apps import AppConfig


class LemmyConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "lemmy"

    def ready(self):
        from . import handlers  # noqa
