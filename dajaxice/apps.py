from django.apps import AppConfig


class DajaxiceConfig(AppConfig):
    name = 'dajaxice'
    verbose_name = 'Dajaxice'
    default_auto_field = 'django.db.models.BigAutoField'

    def ready(self):
        from dajaxice.core import dajaxice_autodiscover
        dajaxice_autodiscover()
