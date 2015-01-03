from django.utils import baseconv
from django.template.defaultfilters import slugify

import time

from unidecode import unidecode


def slugify_uniquely(value, model, slugfield="slug"):
    """
    Returns a slug on a name which is unique within a model's table
    """

    suffix = 0
    potential = base = slugify(unidecode(value))
    if len(potential) == 0:
        potential = 'null'
    while True:
        if suffix:
            potential = "-".join([base, str(suffix)])
        if not model.objects.filter(**{slugfield: potential}).exists():
            return potential
        suffix += 1


def ref_uniquely(a, seq_field,  model, field='ref'):
    album = a.__class__.objects.select_for_update().get(pk=p.pk)
    ref = getattr(album, seq_field) + 1

    while True:
        params = {field: ref, 'album': album}
        if not model.objects.filter(**params).exists():
            setattr(album, seq_field, ref)
            album.save(update_fields=[seq_field])
            return ref

        time.sleep(0.0002)
        ref += 1
