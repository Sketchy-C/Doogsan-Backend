from django.apps import AppConfig


class DoogsanAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'doogsan_app'

    def ready(self):
        import doogsan_app.signals  