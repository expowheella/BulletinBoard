from django.apps import AppConfig


class MyboardappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'myboardapp'

    def ready(self):
        import myboardapp.signals