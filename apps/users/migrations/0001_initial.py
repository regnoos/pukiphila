# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
import django.core.validators
import apps.users.models
from django.conf import settings
import re
import djorm_pgarray.fields


class Migration(migrations.Migration):

    dependencies = [
        ('genres', '0001_initial'),
        ('albumes', '0001_initial'),
        ('auth', '0001_initial'),
        ('country', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('password', models.CharField(verbose_name='password', max_length=128)),
                ('last_login', models.DateTimeField(default=django.utils.timezone.now, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, verbose_name='superuser status', help_text='Designates that this user has all permissions without explicitly assigning them.')),
                ('username', models.CharField(max_length=255, verbose_name='username', validators=[django.core.validators.RegexValidator(re.compile('^[\\w.-]+$', 32), 'Enter a valid username.', 'invalid')], help_text='Required. 30 characters or fewer. Letters, numbers and /./-/_ characters', unique=True)),
                ('email', models.EmailField(verbose_name='email address', max_length=255, blank=True, unique=True)),
                ('birthday', models.DateField(verbose_name='fecha de nacimiento', blank=True, null=True)),
                ('gender', models.CharField(verbose_name='sexo', choices=[('M', 'Hombre'), ('F', 'Mujer')], max_length=1)),
                ('is_active', models.BooleanField(default=True, verbose_name='active', help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.')),
                ('full_name', models.CharField(verbose_name='full name', blank=True, max_length=256)),
                ('bio', models.TextField(default='', verbose_name='biography', blank=True)),
                ('photo', models.ImageField(upload_to=apps.users.models.get_user_file_path, verbose_name='photo', max_length=500, blank=True, null=True)),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('is_staff', models.BooleanField(default=False)),
                ('verificated', models.BooleanField(default=False)),
                ('website', models.URLField(blank=True, null=True)),
                ('profilehits', models.IntegerField(default=0)),
                ('country', models.ForeignKey(to='country.Country', verbose_name='pais', blank=True, null=True)),
                ('followers', models.ManyToManyField(to=settings.AUTH_USER_MODEL, blank=True, related_name='followers_rel_+', null=True)),
                ('genres', models.ManyToManyField(to='genres.Genre')),
                ('groups', models.ManyToManyField(verbose_name='groups', related_query_name='user', related_name='user_set', to='auth.Group', blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of his/her group.')),
                ('user_permissions', models.ManyToManyField(verbose_name='user permissions', related_query_name='user', related_name='user_set', to='auth.Permission', blank=True, help_text='Specific permissions for this user.')),
            ],
            options={
                'verbose_name': 'user',
                'ordering': ['username'],
                'verbose_name_plural': 'users',
                'permissions': (('view_user', 'Can view user'),),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Role',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('name', models.CharField(verbose_name='name', max_length=200)),
                ('slug', models.SlugField(verbose_name='slug', blank=True, max_length=250)),
                ('permissions', djorm_pgarray.fields.TextArrayField(default=[], verbose_name='permissions', dbtype='text', choices=[('view_project', 'View project'), ('view_milestones', 'View milestones'), ('add_milestone', 'Add milestone'), ('modify_milestone', 'Modify milestone'), ('delete_milestone', 'Delete milestone'), ('view_us', 'View user story'), ('add_us', 'Add user story'), ('modify_us', 'Modify user story'), ('delete_us', 'Delete user story'), ('view_tasks', 'View tasks'), ('add_task', 'Add task'), ('modify_task', 'Modify task'), ('delete_task', 'Delete task'), ('view_issues', 'View issues'), ('vote_issues', 'Vote issues'), ('add_issue', 'Add issue'), ('modify_issue', 'Modify issue'), ('delete_issue', 'Delete issue'), ('view_wiki_pages', 'View wiki pages'), ('add_wiki_page', 'Add wiki page'), ('modify_wiki_page', 'Modify wiki page'), ('delete_wiki_page', 'Delete wiki page'), ('view_wiki_links', 'View wiki links'), ('add_wiki_link', 'Add wiki link'), ('modify_wiki_link', 'Modify wiki link'), ('delete_wiki_link', 'Delete wiki link')])),
                ('album', models.ForeignKey(to='albumes.Album', verbose_name='album', related_name='roles', null=True)),
            ],
            options={
                'verbose_name': 'role',
                'ordering': ['slug'],
                'verbose_name_plural': 'roles',
                'permissions': (('view_role', 'Can view role'),),
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='role',
            unique_together=set([('slug', 'album')]),
        ),
    ]
