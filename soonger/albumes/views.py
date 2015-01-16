from rest_framework import viewsets

from soonger.base.api.mixins import DefaultsMixin

from .models import Album
from .serializers import AlbumSerializer


class AlbumViewSet(DefaultsMixin, viewsets.ModelViewSet):
    """API endpoint for listing and creating salbums."""
    queryset = Album.objects.order_by('name')
    serializer_class = AlbumSerializer