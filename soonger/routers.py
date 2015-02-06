from rest_framework.routers import DefaultRouter

from soonger.albumes.views import AlbumViewSet
from soonger.songs.views import SongViewSet
from soonger.users.views import UserViewSet

router = DefaultRouter(trailing_slash=False)
router.register(r'albums', AlbumViewSet)
router.register(r'songs', SongViewSet)
router.register(r'users', UserViewSet)


