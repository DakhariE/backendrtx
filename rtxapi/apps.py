from django.apps import AppConfig


class RtxapiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'rtxapi'

    def ready(self):
        from rtxapi import ping_user
        ping_user.ping()