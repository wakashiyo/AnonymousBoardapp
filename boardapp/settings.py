import os
import environ


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

env = environ.Env()
env.read_env(os.path.join(BASE_DIR, '.env'))

SECRET_KEY = env('SECRET_KEY')

DEBUG = True

# ALLOWED_HOSTS = ['shitsumonbako.com',]
ALLOWED_HOSTS = ['*']


CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True


INSTALLED_APPS = [
    'comments.apps.CommentsConfig',
    'accounts.apps.AccountsConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
    'widget_tweaks',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    # 'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'allauth.account.middleware.AccountMiddleware',
]

INTERNAL_IPS = ("127.0.0.1",)

ROOT_URLCONF = 'boardapp.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'boardapp.wsgi.application'


DATABASES = {
    # 'default': {
    #     'ENGINE': 'django.db.backends.sqlite3',
    #     'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    #     'ATOMIC_REQUESTS': True, # トランザクションを有効にする
    # }
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': env('POSTGRES_DB'),
        'USER': env('POSTGRES_USER'),
        'PASSWORD': env('POSTGRES_PASSWORD'),
        'HOST': env('POSTGRES_HOST'),
        'PORT': env('POSTGRES_PORT'),
    }
}

# Redis cache
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://redis:6379",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
}


AUTHENTICATION_BACKENDS = (
    'allauth.account.auth_backends.AuthenticationBackend',
    'django.contrib.auth.backends.ModelBackend',
)


PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.Argon2PasswordHasher', # Argon2
    'django.contrib.auth.hashers.BCryptSHA256PasswordHasher', # BCrypt
    'django.contrib.auth.hashers.BCryptPasswordHasher', # BCrypt
    'django.contrib.auth.hashers.PBKDF2PasswordHasher', # PBKDF2
    'django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher', # PBKDF2
]

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

SITE_ID = 1
SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = env('SOCIAL_AUTH_GOOGLE_OAUTH2_KEY')
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = env('SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET')
SOCIAL_AUTH_GOOGLE_OAUTH2_USE_UNIQUE_USER_ID = True
CSRF_TRUSTED_ORIGINS = ['https://accounts.google.com']

GOOGLE_SERVICE_ACCOUNT_KEY_FILE = BASE_DIR + '/service_account_credentials.json'
GOOGLE_API_SCOPES = ['https://www.googleapis.com/auth/contacts.readonly']


SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'APP': {
            'client_id': SOCIAL_AUTH_GOOGLE_OAUTH2_KEY,
            'secret': SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET,
            'key': ''
        },
        'SCOPE': [
            'profile',
            'email',
        ],
        'AUTH_PARAMS': {
            'access_type': 'online',
        }
    }
}



LANGUAGE_CODE = 'ja'

TIME_ZONE = 'Asia/Tokyo'

USE_I18N = True

USE_L10N = True

USE_TZ = False




STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

SOCIALACCOUNT_EMAIL_VERIFICATION = "none"
SOCIALACCOUNT_EMAIL_REQUIRED = False
SOCIALACCOUNT_STORE_TOKENS = False
SOCIALACCOUNT_AUTO_SIGNUP = True

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTH_USER_MODEL = 'accounts.CustomUser'
ACCOUNT_AUTHENTICATION_METHOD = 'username'

LOGIN_REDIRECT_URL = '/'
ACCOUNT_LOGOUT_REDIRECT_URL = '/'
ACCOUNT_EMAIL_VERIFICATION = 'none'
ACCOUNT_DEFAULT_HTTP_PROTOCOL='https'