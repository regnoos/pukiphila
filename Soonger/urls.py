from django.conf import settings
from django.conf.urls import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib import admin

urlpatterns = patterns('',
                       # Examples:
                       # url(r'^$', 'Soonger.views.home', name='home'),
                       # url(r'^blog/', include('blog.urls')),
                       url(r'^', include('apps.home.urls')),
                       url(r'^', include('apps.users.urls', namespace='users', app_name='users')),
                       url(r'^', include('apps.albumes.urls', namespace='albums', app_name='albumes')),
                       url(r'^admin/', include(admin.site.urls)),

                       # # static
                       # (r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': STATIC_ROOT}),
                       #
                       # # media
                       # (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': MEDIA_ROOT}),
                       )


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
