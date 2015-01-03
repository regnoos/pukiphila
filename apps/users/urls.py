from django.conf.urls import patterns, include, url

from .views import UserProfileView, ArtistProfileView, ArtistListView


urlpatterns = patterns('',
                       url(r'^signup/$', 'apps.users.views.signup', name='signup'),
                       url(r'^signin/$', 'django.contrib.auth.views.login',
                           {'template_name': 'users/signin.html'}, name='signin'),
                       url(r'^logout/$', 'django.contrib.auth.views.logout_then_login',
                           name='logout'),
                       url(r'^artists/$', ArtistListView.as_view(), name='artist_list'),
                       url(r'^artists/(?P<slug>[-\w]+)/$', ArtistProfileView.as_view(), name='artist_profile'),
                       url(r'^users/(?P<slug>[-\w]+)/$', UserProfileView.as_view(), name='user_profile')
                       )


