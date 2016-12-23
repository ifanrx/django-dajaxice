try:
    from django.conf.urls import include, url
except ImportError:
    from django.conf.urls.defaults import include, url

from dajaxice.core import dajaxice_autodiscover, dajaxice_config

dajaxice_autodiscover()

urlpatterns = [
    url(dajaxice_config.dajaxice_url, include('dajaxice.urls')),
   ]
