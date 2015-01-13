from django.conf import settings
from django.conf.urls import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    url(r'^api/token/', obtain_auth_token, name='api-token'),
]


def mediafiles_urlpatterns(prefix):
    """
    Method for serve media files with runserver.
    """
    import re
    from django.views.static import serve

    return [
        url(r'^%s(?P<path>.*)$' % re.escape(prefix.lstrip('/')), serve,
            {'document_root': settings.MEDIA_ROOT})
    ]

if settings.DEBUG:
    # Hardcoded only for development server
    urlpatterns += staticfiles_urlpatterns(prefix="/static/")
    urlpatterns += mediafiles_urlpatterns(prefix="/media/")
