from django.conf.urls import include, patterns, url
from django.conf import settings


urlpatterns = patterns(
    '',
    url(r'', include('multi_cookies.urls')),
    url(r'', include('lms.urls')),
)
