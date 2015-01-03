# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
import djorm_pgarray.fields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Album',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('name', models.CharField(verbose_name='name', max_length=250)),
                ('slug', models.SlugField(max_length=250, verbose_name='slug', blank=True, unique=True)),
                ('releasedate', models.DateField(verbose_name='date release', blank=True)),
                ('description', models.TextField(verbose_name='description')),
                ('thumb', models.ImageField(verbose_name='album pic', upload_to='img')),
                ('created_date', models.DateTimeField(default=django.utils.timezone.now, verbose_name='created date')),
                ('modified_date', models.DateTimeField(verbose_name='modified date')),
                ('anon_permissions', djorm_pgarray.fields.TextArrayField(default=[], verbose_name='anonymous permissions', dbtype='text', choices=[('view_project', 'View project'), ('view_milestones', 'View milestones'), ('view_us', 'View user stories'), ('view_tasks', 'View tasks'), ('view_issues', 'View issues'), ('view_wiki_pages', 'View wiki pages'), ('view_wiki_links', 'View wiki links')])),
                ('public_permissions', djorm_pgarray.fields.TextArrayField(default=[], verbose_name='user permissions', dbtype='text', choices=[('view_project', 'View project'), ('view_milestones', 'View milestones'), ('view_us', 'View user stories'), ('view_issues', 'View issues'), ('vote_issues', 'Vote issues'), ('view_tasks', 'View tasks'), ('view_wiki_pages', 'View wiki pages'), ('view_wiki_links', 'View wiki links'), ('request_membership', 'Request membership'), ('add_us_to_project', 'Add user story to project'), ('add_comments_to_us', 'Add comments to user stories'), ('add_comments_to_task', 'Add comments to tasks'), ('add_issue', 'Add issues'), ('add_comments_issue', 'Add comments to issues'), ('add_wiki_page', 'Add wiki page'), ('modify_wiki_page', 'Modify wiki page'), ('add_wiki_link', 'Add wiki link'), ('modify_wiki_link', 'Modify wiki link')])),
                ('is_private', models.BooleanField(default=False, verbose_name='is private')),
            ],
            options={
                'verbose_name': 'album',
                'ordering': ['name'],
                'verbose_name_plural': 'albumes',
                'permissions': (('view_project', 'Can view project'),),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Membership',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('is_owner', models.BooleanField(default=False)),
                ('email', models.EmailField(default=None, verbose_name='email', max_length=255, blank=True, null=True)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, verbose_name='creado el')),
                ('album', models.ForeignKey(to='albumes.Album', related_name='memberships')),
            ],
            options={
                'verbose_name': 'membership',
                'ordering': ['album', 'user__full_name', 'user__username', 'user__email', 'email'],
                'verbose_name_plural': 'membershipss',
                'permissions': (('view_membership', 'Can view membership'),),
            },
            bases=(models.Model,),
        ),
    ]
