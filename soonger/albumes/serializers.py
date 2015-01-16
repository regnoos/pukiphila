from rest_framework import serializers
from rest_framework.reverse import reverse

from soonger.users.models import User
from soonger.users.serializers import UserSerializer
from .models import Album


class ArtistListingField(serializers.RelatedField):

    def to_internal_value(self, data):
        pass

    def to_representation(self, value):
        request = self.context['request']
        return {
            'name': '%s' % (value.full_name,),
            'url': reverse('user-detail', kwargs={User.USERNAME_FIELD: value.username}, request=request),

        }


class SongListingField(serializers.RelatedField):

    def to_internal_value(self, data):
        pass

    def to_representation(self, value):
        request = self.context['request']
        return {
            'title': '%s' % (value.title,),
            'url': reverse('song-detail', kwargs={'pk': value.pk}, request=request),
        }


class AlbumSerializer(serializers.ModelSerializer):
    links = serializers.SerializerMethodField()
    songs = SongListingField(many=True, read_only=True)
    owner = UserSerializer(read_only=True)
    members = ArtistListingField(many=True, read_only=True)

    class Meta:
        model = Album
        fields = ('id', 'name', 'slug', 'releasedate', 'description', 'thumb', 'created_date', 'modified_date', 'owner',
                  'members', 'is_private', 'links', 'songs',)

    def get_links(self, obj):
        request = self.context['request']
        return {
            'self': reverse('album-detail', kwargs={'pk': obj.pk}, request=request),
            'songs': reverse('song-list', request=request) + '?album={}'.format(obj.pk),
        }