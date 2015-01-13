from django.db import models


class Genre(models.Model):
    name = models.CharField(max_length=30, verbose_name='nombre')

    class Meta:
        db_table = 'genres'
        verbose_name = 'genero'
        verbose_name_plural = 'Generos'

    def __str__(self):
        return self.name
