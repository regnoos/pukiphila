# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Genre',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('name', models.CharField(verbose_name='nombre', max_length=30)),
            ],
            options={
                'verbose_name': 'genero',
                'verbose_name_plural': 'Generos',
                'db_table': 'genres',
            },
            bases=(models.Model,),
        ),
    ]
