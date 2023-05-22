from django.apps import AppConfig


class ClientappConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "clientApp"
    def ready(self):
        from .scheduler import schedule_mails
        schedule_mails.start()
