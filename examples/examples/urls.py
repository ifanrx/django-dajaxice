from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import include, re_path

from dajaxice.core import dajaxice_autodiscover, dajaxice_config
from simple import views as simple_views

dajaxice_autodiscover()

urlpatterns = [
    re_path(dajaxice_config.dajaxice_url, include('dajaxice.urls')),
    re_path(r'^$', simple_views.index, name='index'),
]

urlpatterns += staticfiles_urlpatterns()
