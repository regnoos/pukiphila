# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Country',
            fields=[
                ('keycountry', models.CharField(serialize=False, primary_key=True, max_length=3)),
                ('name', models.CharField(verbose_name='nombre', max_length=50)),
            ],
            options={
                'verbose_name': 'país',
                'verbose_name_plural': 'Paises',
                'db_table': 'countries',
            },
            bases=(models.Model,),
        ),
    ]
