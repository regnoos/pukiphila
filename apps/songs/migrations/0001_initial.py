# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('genres', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('albumes', '0002_auto_20141212_0544'),
    ]

    operations = [
        migrations.CreateModel(
            name='Song',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('title', models.CharField(max_length=150, verbose_name='titulo')),
                ('slug', models.SlugField(help_text='Valor para la album page URL, creado a partir del nombre', max_length=150)),
                ('urlpath', models.FileField(upload_to='song', verbose_name='ruta de la cancion')),
                ('releasedate', models.DateField(verbose_name='año')),
                ('created', models.DateField(auto_now_add=True)),
                ('hits', models.IntegerField(blank=True, null=True)),
                ('like', models.IntegerField(blank=True, null=True)),
                ('album', models.ForeignKey(to='albumes.Album', blank=True, related_name='song', null=True)),
                ('artist', models.ManyToManyField(verbose_name='artists', related_name='featuring', to=settings.AUTH_USER_MODEL)),
                ('genre', models.ManyToManyField(verbose_name='genero', related_name='genres', to='genres.Genre')),
            ],
            options={
                'verbose_name': 'song',
                'verbose_name_plural': 'songs',
                'db_table': 'song',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('nombre', models.CharField(max_length=50)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='song',
            name='tags',
            field=models.ManyToManyField(verbose_name='tags', related_name='songs', to='songs.Tag'),
            preserve_default=True,
        ),
    ]
