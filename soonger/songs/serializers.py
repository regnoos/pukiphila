from rest_framework import serializers
from rest_framework.reverse import reverse

from .models import Song


class SongSerializer(serializers.ModelSerializer):
    links = serializers.SerializerMethodField()

    class Meta:
        model = Song
        fields = ('id', 'title', 'slug', 'urlpath', 'artist', 'releasedate', 'tags', 'album', 'created', 'genre',
                  'hits', 'like', 'links',)

    def get_links(self, obj):
        request = self.context['request']
        return {
            'self': reverse('song-detail', kwargs={'pk': obj.pk}, request=request),
        }