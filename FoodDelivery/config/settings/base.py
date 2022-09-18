import environ

env = environ.Env()
environ.Env.read_env()

root = environ.Path(__file__) - 3

apps_root = root.path('food_delivery')

BASE_DIR = root()

SECRET_KEY = env('SECRET_KEY')

DJANGO_APPS = [
    # "admin_interface",  # This is use for admin panel modify
    # "flat_responsive",  # only if django version < 2.0
    # "flat",  # only if django version < 1.9
    # "colorfield",  # This is use for admin panel modify
    # 'jazzmin',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]


#UDRT INSTALLED APPS
THIRD_PARTY_APPS = [
    'rest_framework',
    'drf_secure_token',
    'django_filters',
    'crispy_forms',

]

#USER MODELS APPS
LOCAL_APPS = [
    'food_delivery.custom_auth',
    'food_delivery.registrations',
    'food_delivery.product',
    # 'food_delivery.cart',

]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS



MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

PROJECT_FULL_NAME = env('PROJECT_FULL_NAME', default='FoodDelivery')

AUTH_USER_MODEL = 'custom_auth.ApplicationUser'

AUTHENTICATION_BACKENDS = (
    'food_delivery.custom_auth.auth_backends.model_backend.CustomModelBackend',
)

# Django rest framework configuration

from rest_framework.permissions import IsAuthenticated

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'drf_secure_token.authentication.SecureTokenAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_FILTER_BACKENDS': (
        'django_filters.rest_framework.DjangoFilterBackend',
    ),
    'PAGE_SIZE': 10,
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',

}


TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [root('food_delivery', 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

STATIC_URL = '/static/'
STATIC_ROOT = root('static')

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'django.contrib.staticfiles.finders.FileSystemFinder',
)

STATICFILES_DIRS = [
    root('food_delivery', 'assets'),
]

MEDIA_URL = '/media/'
MEDIA_ROOT = root('media')

USER_PHOTO_PATH = 'user_photos'

FOOD_PHOTO_PATH = 'food_photos'
POST_RESTAURANT_PATH = 'restaurant_photos'

LOGIN_REDIRECT_URL = 'web_auth:index'
CRISPY_TEMPLATE_PACK = 'bootstrap4'


# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
