from django.db import models

from soonger.users.models import User
from soonger.albumes.models import Album
from soonger.genres.models import Genre


class Tag(models.Model):
    nombre = models.CharField(max_length=50)

    def __str__(self):
        return self.nombre


class Song(models.Model):
    title = models.CharField(max_length=150, verbose_name='titulo')
    slug = models.SlugField(max_length=150, help_text='Valor para la album page URL, creado a partir del nombre')
    urlpath = models.FileField(upload_to='song', verbose_name='ruta de la cancion')
    artist = models.ManyToManyField(User, verbose_name='artists', related_name='featuring')
    releasedate = models.DateField(verbose_name='año')
    tags = models.ManyToManyField(Tag, verbose_name='tags', related_name='songs')
    album = models.ForeignKey(Album, related_name='songs', blank=True, null=True)
    created = models.DateField(auto_now_add=True)
    genre = models.ManyToManyField(Genre, verbose_name='genero', related_name='genres')
    hits = models.IntegerField(blank=True, null=True)
    like = models.IntegerField(blank=True, null=True)

    class Meta:
        db_table = 'song'
        verbose_name = 'song'
        verbose_name_plural = 'songs'

    # @models.permalink
    # def get_absolute_url(self):
    #     return 'catalog_song', (), {'song_slug': self.slug}

    def __str__(self):
        return self.title