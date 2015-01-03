from Soonger.settings import base
from django.core.urlresolvers import reverse


def soonger(request):
    return {'site_name': base.SITE_NAME, 'meta_keywords': base.META_KEYWORDS,
            'meta_description': base.META_DESCRIPTION, 'request': request}


def home_menu(request):
    menu = {'menu': [
        {'name': 'Inicio', 'url': reverse('/')},
        {'name': 'Albums', 'url': '/albums'},
    ]}

    for item in menu['menu']:
        if request.path == item['url']:
            item['active'] = True
    return menu
