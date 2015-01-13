from django.core.exceptions import ValidationError
from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone

from djorm_pgarray.fields import TextArrayField

from soonger.users.models import User
from soonger.permissions.permissions import ANON_PERMISSIONS, USER_PERMISSIONS
from soonger.users.models import Role
from soonger.base.utils.slug import slugify_uniquely
from soonger.base.utils.sequence import arithmetic_progression


class Membership(models.Model):
    # This model stores all album memberships. Also
    # stores invitations to memberships that does not have
    # assigned user.
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, default=None,
                             related_name="memberships")
    album = models.ForeignKey('Album', null=False, blank=False, related_name="memberships")
    role = models.ForeignKey(Role, null=False, blank=False,
                             related_name="memberships")
    is_owner = models.BooleanField(default=False, null=False, blank=False)

    # Invitation metadata
    email = models.EmailField(max_length=255, default=None, null=True, blank=True,
                              verbose_name=_("email"))
    created_at = models.DateTimeField(default=timezone.now,
                                      verbose_name=_("creado el"))

    invited_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="ihaveinvited+",
                                   null=True, blank=True)

    def clean(self):
        # TODO: Review and do it more robust
        memberships = Membership.objects.filter(user=self.user, album=self.album)
        if self.user and memberships.count() > 0 and memberships[0].id != self.id:
            raise ValidationError(_('The user is already member of the album'))

    class Meta:
        verbose_name = "membership"
        verbose_name_plural = "membershipss"
        unique_together = ("user", "album",)
        ordering = ["album", "user__full_name", "user__username", "user__email", "email"]
        permissions = (
            ("view_membership", "Can view membership"),
        )


class Album(models.Model):
    name = models.CharField(max_length=250, null=False, blank=False, verbose_name=_("name"))
    slug = models.SlugField(max_length=250, unique=True, null=False, blank=True, verbose_name=_("slug"))
    releasedate = models.DateField(null=False, blank=True, verbose_name=_("date release"))
    description = models.TextField(null=False, blank=False, verbose_name=_("description"))
    thumb = models.ImageField(upload_to='album_pic', verbose_name='thumb')
    created_date = models.DateTimeField(null=False, blank=False, verbose_name=_("created date"), default=timezone.now)
    modified_date = models.DateTimeField(null=False, blank=False, verbose_name=_("modified date"))
    owner = models.ForeignKey(User, null=False, blank=False, related_name="owned_albumes",
                              verbose_name=_("owner"))
    members = models.ManyToManyField(User, related_name="albumes",
                                     through="Membership", verbose_name=_("members"),
                                     through_fields=("album", "user"))
    anon_permissions = TextArrayField(blank=True, null=True,
                                      default=[],
                                      verbose_name=_("anonymous permissions"),
                                      choices=ANON_PERMISSIONS)
    public_permissions = TextArrayField(blank=True, null=True,
                                        default=[],
                                        verbose_name=_("user permissions"),
                                        choices=USER_PERMISSIONS)
    is_private = models.BooleanField(default=False, null=False, blank=True,
                                     verbose_name=_("is private"))

    _importing = None

    class Meta:
        verbose_name = "album"
        verbose_name_plural = "albumes"
        ordering = ["name"]
        permissions = (
            ("view_project", "Can view project"),
        )

    def __str__(self):
        return self.name

    # def __repr__(self):
    #     return "<Album {0}>".format(self.id)

    def save(self, *args, **kwargs):
        if not self._importing or not self.modified_date:
            self.modified_date = timezone.now()

        if not self.slug:
            base_name = "{}-{}".format(self.owner.username, self.name)
            base_slug = slugify_uniquely(base_name, self.__class__)
            slug = base_slug
            for i in arithmetic_progression():
                if not type(self).objects.filter(slug=slug).exists() or i > 100:
                    break
                slug = "{}-{}".format(base_slug, i)
            self.slug = slug

        super().save(*args, **kwargs)

    def get_roles(self):
        return self.roles.all()

    def get_users(self):
        user_model = get_user_model()
        members = self.memberships.values_list("user", flat=True)
        return user_model.objects.filter(id__in=list(members))