from django.views.generic import ListView, DetailView

from .models import Album
from apps.songs.models import Song


class AlbumListView(ListView):
    model = Album
    context_object_name = 'albumes'

    paginate_by = 12


class AlbumDetailView(DetailView):
    model = Album
    context_object_name = 'album'

    def get_context_data(self, **kwargs):
        context = super(AlbumDetailView, self).get_context_data(**kwargs)
        songs = Song.objects.filter(album=context['object']).order_by('created')
        tags = [song.tags.all() for song in songs]

        # users = User.objects.filter(members=context['object'])
        # albums = [user.albumes.all() for user in users]

        context['tags'] = tags
        context['songs'] = songs

        return context