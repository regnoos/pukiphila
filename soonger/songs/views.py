from rest_framework import viewsets

from soonger.base.api.mixins import DefaultsMixin

from .models import Song
from .serializers import SongSerializer


class SongViewSet(DefaultsMixin, viewsets.ModelViewSet):
    """API endpoint for listing and creating songs."""

    queryset = Song.objects.all()
    serializer_class = SongSerializer
