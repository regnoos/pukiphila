# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('albumes', '0001_initial'),
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='membership',
            name='invited_by',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='ihaveinvited+', blank=True, null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='membership',
            name='role',
            field=models.ForeignKey(to='users.Role', related_name='memberships'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='membership',
            name='user',
            field=models.ForeignKey(default=None, to=settings.AUTH_USER_MODEL, related_name='memberships', blank=True, null=True),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='membership',
            unique_together=set([('user', 'album')]),
        ),
        migrations.AddField(
            model_name='album',
            name='members',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL, verbose_name='members', through='albumes.Membership', related_name='albumes'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='album',
            name='owner',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, verbose_name='owner', related_name='owned_albumes'),
            preserve_default=True,
        ),
    ]
