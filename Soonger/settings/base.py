# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
from unipath import Path
from django.conf.global_settings import TEMPLATE_CONTEXT_PROCESSORS as TCP, TEMPLATE_LOADERS as TL, STATICFILES_FINDERS as SF
BASE_DIR = Path(__file__).ancestor(3)

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'x(-ah=ymsgs&-y4$sdl!_&g79_&a(ir+mdp-yb8(hny7bckg$^'

from django.core.urlresolvers import reverse_lazy

LOGIN_URL = reverse_lazy('users:signin')
LOGIN_REDIRECT_URL = reverse_lazy('home')
LOGOUT_URL = reverse_lazy('users:logout')

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.staticfiles',
    # 'django.contrib.admin',

    # Third party apps
    'autofixture',
    'rest_framework',
    'rest_framework.authtoken',

    # Internal apps
    'apps.home',
    'apps.base',
    'apps.permissions',
    'apps.country',
    'apps.genres',
    'apps.users',
    'apps.albumes',
    'apps.songs',

)

TEMPLATE_LOADERS = TL + (
    'django.template.loaders.eggs.Loader',
)

TEMPLATE_CONTEXT_PROCESSORS = TCP + (
    'django.core.context_processors.csrf',
    'django.core.context_processors.request',
    # 'apps.utils.context_processors.home_menu',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'Soonger.urls'

WSGI_APPLICATION = 'Soonger.wsgi.application'

AUTH_USER_MODEL = "users.User"

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

TEMPLATE_DIRS = [BASE_DIR.child('templates')]

SITE_NAME = 'Soonger!'
META_KEYWORDS = 'Music, soonger, music new, musician best, music free'
META_DESCRIPTION = 'Website to listen to good music in a fast and secure. Especially for free.'