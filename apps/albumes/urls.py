from django.conf.urls import patterns, url

from .views import AlbumListView, AlbumDetailView


urlpatterns = patterns('',
                       url(r'^albums/$', AlbumListView.as_view(), name='album_list'),
                       url(r'^albums/(?P<pk>[0-9]+)$', AlbumDetailView.as_view(), name='album_detail')
                       )

