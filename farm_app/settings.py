import os
from pathlib import Path
from django.core.management.utils import get_random_secret_key
import environ
import dj_database_url
import django_heroku



BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-@e0r%+2z5_c$%h(o_f4y6g(&)=iee$zq+3awp=*wdf$#n_yr(p'

DEBUG = True

ALLOWED_HOSTS = ['farm-app-737afdcdcda2.herokuapp.com', 'localhost', '127.0.0.1']


# CSRF_TRUSTED_ORIGINS = [f'http://{x}:81' for x in ALLOWED_HOSTS]
CSRF_TRUSTED_ORIGINS = ['http://localhost', 'http://127.0.0.1']


SESSION_COOKIE_AGE = 86400
CART_SESSION_ID = 'cart'
STRIPE_KEY_ID_PUBLISHABLE = ''


INSTALLED_APPS = [
    'farm_app.accounts',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'whitenoise.runserver_nostatic',

    'farm_app.catalog',
    'farm_app.cart',
    'farm_app.order',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

MIDDLEWARE.insert(1, 'whitenoise.middleware.WhiteNoiseMiddleware')


ROOT_URLCONF = 'farm_app.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates']
        ,
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.media',
                'farm_app.cart.context_processors.cart',

            ],
        },
    },
]

WSGI_APPLICATION = 'farm_app.wsgi.application'

# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql_psycopg2',
#         'NAME': 'd6oqkpcqg36s6t',
#         'USER': 'uapfi41aogr9q9',
#         'PASSWORD': 'p01b3e060b30342f735b778c7faa44c2889f51319b3a2fa08e6d9915fa8b90848',
#         'HOST': 'ccaml3dimis7eh.cluster-czz5s0kz4scl.eu-west-1.rds.amazonaws.com',
#         'PORT': '5432',
#     }
# }
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/


STATIC_ROOT = BASE_DIR / 'staticfiles'

STATIC_URL = '/static/'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
STATICFILES_DIRS = [
    BASE_DIR / "static",
]

django_heroku.settings(locals())

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTH_USER_MODEL = 'accounts.FarmerUser'

LOGIN_REDIRECT_URL = 'home'
LOGOUT_REDIRECT_URL = 'login'
LOGIN_URL = '/accounts/login/'
