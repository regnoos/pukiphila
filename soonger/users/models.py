import hashlib
import os
import os.path as path
import re

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser, UserManager, PermissionsMixin
from django.core import validators
from django.utils import timezone
from django.utils.encoding import force_bytes
from django.dispatch import receiver

from djorm_pgarray.fields import TextArrayField

from soonger.genres.models import Genre
from soonger.country.models import Country
from soonger.base.utils.iterators import split_by_n
from soonger.base.utils.slug import slugify_uniquely
from soonger.permissions.permissions import MEMBERS_PERMISSIONS


def get_user_file_path(instance, filename):
    basename = path.basename(filename).lower()

    hs = hashlib.sha256()
    hs.update(force_bytes(timezone.now().isoformat()))
    hs.update(os.urandom(1024))

    p1, p2, p3, p4, *p5 = split_by_n(hs.hexdigest(), 1)
    hash_part = path.join(p1, p2, p3, p4, "".join(p5))

    return path.join("user", hash_part, basename)


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(_('username'), max_length=255, unique=True,
                                help_text=_('Required. 30 characters or fewer. Letters, numbers and '
                                            '/./-/_ characters'),
                                validators=[validators.RegexValidator(re.compile('^[\w.-]+$'),
                                                                      _('Enter a valid username.'), 'invalid')
                                            ])
    email = models.EmailField(_('email address'), max_length=255, blank=True, unique=True)
    birthday = models.DateField(verbose_name='fecha de nacimiento', blank=True, null=True)
    gender = models.CharField(max_length=1, choices=((u'M', 'Hombre'), (u'F', 'Mujer'),), verbose_name='sexo')
    country = models.ForeignKey(Country, verbose_name='pais', blank=True, null=True)
    is_active = models.BooleanField(_('active'), default=True, help_text=_('Designates whether this user should be '
                                                                           'treated as active. Unselect this instead of'
                                                                           ' deleting accounts.'))

    full_name = models.CharField(_('full name'), max_length=256, blank=True)
    bio = models.TextField(null=False, blank=True, default="", verbose_name=_("biography"))
    photo = models.ImageField(upload_to='avatar', max_length=500, null=True, blank=True,
                              verbose_name=_("photo"))
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)
    is_staff = models.BooleanField(default=False)
    followers = models.ManyToManyField('self', blank=True, null=True, related_name='followers')
    verificated = models.BooleanField(default=False)
    website = models.URLField(blank=True, null=True)
    profilehits = models.IntegerField(default=0)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    objects = UserManager()

    class Meta:
        verbose_name = "user"
        verbose_name_plural = "users"
        ordering = ["username"]
        permissions = (
            ("view_user", "Can view user"),
        )

    def __str__(self):
        return self.get_full_name()

    def get_short_name(self):
        return self.username

    def get_full_name(self):
        return self.full_name or self.username or self.email


class Role(models.Model):
    name = models.CharField(max_length=200, null=False, blank=False,
                            verbose_name=_("name"))
    slug = models.SlugField(max_length=250, null=False, blank=True,
                            verbose_name=_("slug"))
    permissions = TextArrayField(blank=True, null=True,
                                 default=[],
                                 verbose_name=_("permissions"),
                                 choices=MEMBERS_PERMISSIONS)
    # null=True is for make work django 1.7 migrations. project
    # field causes some circular dependencies, and due to this
    # it can not be serialized in one transactional migration.
    album = models.ForeignKey("albumes.Album", null=True, blank=False,
                              related_name="roles", verbose_name=_("album"))

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify_uniquely(self.name, self.__class__)

        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "role"
        verbose_name_plural = "roles"
        ordering = ["slug"]
        unique_together = (("slug", "album"),)
        permissions = (
            ("view_role", "Can view role"),
        )

    def __str__(self):
        return self.name