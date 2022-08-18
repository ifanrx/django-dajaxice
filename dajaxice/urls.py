from django.urls import re_path
from .views import DajaxiceRequest


urlpatterns = [
    re_path(r'^(.+)/$', DajaxiceRequest.as_view(), name='dajaxice-call-endpoint'),
    re_path(r'', DajaxiceRequest.as_view(), name='dajaxice-endpoint'),
]
