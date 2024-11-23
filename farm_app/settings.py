import os
from pathlib import Path
from django.core.management.utils import get_random_secret_key
import environ
import dj_database_url
import django_heroku
import environ


BASE_DIR = Path(__file__).resolve().parent.parent



SECRET_KEY =  os.getenv('SECRET_KEY', '87$-yv5gv-vszmuj_l8k8vrdd7x91iwmjs^^71janp6$l2o1no')


DEBUG =  os.getenv('DEBUG', default=False)

ALLOWED_HOSTS = ['farm-app-737afdcdcda2.herokuapp.com', 'localhost', '127.0.0.1']


CSRF_TRUSTED_ORIGINS = [f'http://{x}:81' for x in ALLOWED_HOSTS]


SESSION_COOKIE_AGE = 86400
CART_SESSION_ID = 'cart'
STRIPE_KEY_ID_PUBLISHABLE = ''


INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'whitenoise.runserver_nostatic',
    'farm_app.accounts',
    'farm_app.catalog',
    'farm_app.cart',
    'farm_app.order',
    'cloudinary',
    'cloudinary_storage',
]
CLOUDINARY_STORAGE = {
    'CLOUD_NAME': os.getenv('CLOUD_NAME', None),
    'API_KEY': os.getenv('API_KEY', None),
    'API_SECRET': os.getenv('API_SECRET', None),
}

COLLECTSTATIC_IGNORE = [
    'admin/css/*',
    'admin/img/*',
    'admin/js/*',
]


DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'




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


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.getenv('DB_NAME', 'None'),
        'USER': os.getenv('DB_USER', 'None'),
        'PASSWORD': os.getenv('DB_PASSWORD', 'None'),
        'HOST': os.getenv('DB_HOST', 'None'),
        'PORT': os.getenv('DB_PORT', 5432),
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
LOGOUT_REDIRECT_URL = 'home'
LOGIN_URL = '/accounts/login/'
