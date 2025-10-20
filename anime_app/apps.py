from django.apps import AppConfig

class AnimeAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'anime_app'

    def ready(self):
        import anime_app.signals
