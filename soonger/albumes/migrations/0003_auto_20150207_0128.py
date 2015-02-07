# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('albumes', '0002_auto_20141212_0544'),
    ]

    operations = [
        migrations.AlterField(
            model_name='album',
            name='created_date',
            field=models.DateField(verbose_name='created date', default=django.utils.timezone.now),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='album',
            name='modified_date',
            field=models.DateField(verbose_name='modified date'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='album',
            name='thumb',
            field=models.ImageField(verbose_name='thumb', upload_to='album_pic'),
            preserve_default=True,
        ),
    ]
