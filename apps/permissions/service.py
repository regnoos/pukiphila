from apps.albumes.models import Membership, Album
from .permissions import OWNERS_PERMISSIONS, MEMBERS_PERMISSIONS, ANON_PERMISSIONS, USER_PERMISSIONS


def _get_user_album_membership(user, album):
    if user.is_anonymous():
        return None

    try:
        return Membership.objects.get(user=user, album=album)
    except Membership.DoesNotExist:
        return None


def _get_object_album(obj):
    album = None

    if isinstance(obj, Album):
        album = obj
    elif obj and hasattr(obj, 'album'):
        album = obj.album
    return album


def is_album_owner(user, obj):
    if user.is_superuser:
        return True

    album = _get_object_album(obj)

    if album and album.owner == user:
        return True

    membership = _get_user_album_membership(user, album)
    if membership and membership.is_owner:
        return True

    return False


def user_has_perm(user, perm, obj=None):
    album = _get_object_album(obj)

    if not album:
        return False

    return perm in get_user_album_permissions(user, album)


def role_has_perm(role, perm):
    return perm in role.permissions


def _get_membership_permissions(membership):
    if membership and membership.role and membership.role.permissions:
        return membership.role.permissions
    return []


def get_user_album_permissions(user, album):
    membership = _get_user_album_membership(user, album)
    if user.is_superuser:
        owner_permissions = list(map(lambda perm: perm[0], OWNERS_PERMISSIONS))
        members_permissions = list(map(lambda perm: perm[0], MEMBERS_PERMISSIONS))
        public_permissions = list(map(lambda perm: perm[0], USER_PERMISSIONS))
        anon_permissions = list(map(lambda perm: perm[0], ANON_PERMISSIONS))
    elif album.owner == user:
        owner_permissions = list(map(lambda perm: perm[0], OWNERS_PERMISSIONS))
        members_permissions = list(map(lambda perm: perm[0], MEMBERS_PERMISSIONS))
        public_permissions = album.public_permissions if album.public_permissions is not None else []
        anon_permissions = album.anon_permissions if album.anon_permissions is not None else []
    elif membership:
        if membership.is_owner:
            owner_permissions = list(map(lambda perm: perm[0], OWNERS_PERMISSIONS))
        else:
            owner_permissions = []
        members_permissions = _get_membership_permissions(membership)
        public_permissions = album.public_permissions if album.public_permissions is not None else []
        anon_permissions = album.anon_permissions if album.anon_permissions is not None else []
    elif user.is_authenticated():
        owner_permissions = []
        members_permissions = []
        public_permissions = album.public_permissions if album.public_permissions is not None else []
        anon_permissions = album.anon_permissions if album.anon_permissions is not None else []
    else:
        owner_permissions = []
        members_permissions = []
        public_permissions = []
        anon_permissions = album.anon_permissions if album.anon_permissions is not None else []

    return set(owner_permissions + members_permissions + public_permissions + anon_permissions)
