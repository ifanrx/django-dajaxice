from django.urls import include, re_path

from dajaxice.core import dajaxice_autodiscover, dajaxice_config

dajaxice_autodiscover()

urlpatterns = [
    #Dajaxice URLS
    re_path(dajaxice_config.dajaxice_url, include('dajaxice.urls')),
]
