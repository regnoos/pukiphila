from django.conf.urls import patterns, include, url

from .views import UserProfileView, ArtistProfileView, ArtistListView, UserListenView, UserVideoView, \
    UserVideoDetailView, EventListView, GenreListView


urlpatterns = patterns('',
                       url(r'^signup/$', 'soonger.users.views.signup', name='signup'),
                       url(r'^signin/$', 'django.contrib.auth.views.login',
                           {'template_name': 'users/signin.html'}, name='signin'),
                       url(r'^logout/$', 'django.contrib.auth.views.logout_then_login',
                           name='logout'),
                       url(r'^artists/$', ArtistListView.as_view(), name='artist_list'),
                       url(r'^artists/(?P<slug>[-\w]+)/$', ArtistProfileView.as_view(), name='artist_profile'),
                       url(r'^users/(?P<slug>[-\w]+)/$', UserProfileView.as_view(), name='user_profile'),
                       url(r'^listen/$', UserListenView.as_view(), name='user_listen'),
                       url(r'^videos/$', UserVideoView.as_view(), name='user_videos'),
                       url(r'^videos/detalle$', UserVideoDetailView.as_view(), name='video_detail'),
                       url(r'^eventos/$', EventListView.as_view(), name='event_list'),
                       url(r'^generos/$', GenreListView.as_view(), name='genre_list'),
                       )


