import environ, os
from pprint import pprint
from pathlib import Path
from datetime import timedelta

env = environ.Env()
environ.Env.read_env()

BASE_DIR = Path(__file__).resolve().parent.parent.parent
DEBUG = True

ALLOWED_HOSTS = [
    '*'
    ]
SECRET_KEY = env("SECRET_KEY")

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

PROJECT_APPS = [
    'app.apps.AppConfig',
    'users.apps.UsersConfig'
]

INSTALLED_PACKAGES = [
    'rest_framework',
    "corsheaders",
    'rest_framework_simplejwt.token_blacklist',
    'drf_yasg',
    'drf_spectacular',
    'debug_toolbar',
    'django_extensions',
]

INSTALLED_APPS += PROJECT_APPS + INSTALLED_PACKAGES

INTERNAL_IPS = [
    "127.0.0.1",
]


MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    "debug_toolbar.middleware.DebugToolbarMiddleware",
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

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

WSGI_APPLICATION = 'talent_score.wsgi.application'


LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

ROOT_URLCONF = 'talent_score.urls'

AUTH_USER_MODEL = 'users.UserAccount'



REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        # 'rest_framework_simplejwt.authentication.JWTAuthentication', # TODO: For now
        'users.authenticate.CustomAuthentication',
    ],

    "DEFAULT_PERMISSION_CLASSES": [
        'rest_framework.permissions.AllowAny',
    ],
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',

}
# CORS_ALLOWED_ORIGINS = [
#     'http://localhost:3000',
#     'http://localhost:5174',
#     'http://127.0.0.1:5173',
#     'http://localhost:5173',
#     'https://talent-scoring-frontend.vercel.app',
#     'https://talent-scoring-frontend-fikaroo.vercel.app',
#     'https://talent-scoring-frontend-git-main-fikaroo.vercel.app',
#     'https://talentscoring.vercel.app',
#     'https://talent-score-front-end-deploy-noi3.vercel.app',
#     'https://talentscore-report.netlify.app',
#     'https://talent-score.vercel.app'
# ]
CORS_ALLOW_CREDENTIALS = True
CSRF_COOKIE_SECURE = True
CSRF_COOKIE_HTTP_ONLY = True
CORS_ALLOW_ALL_ORIGINS = True
CSRF_TRUSTED_ORIGINS = [
    'http://localhost:3000',
    'http://127.0.0.1:5173',
    'http://localhost:5173',
    'http://localhost:5174',
    'https://talent-score-front-end-deploy-noi3.vercel.app',
    'https://talent-score.vercel.app',
    'https://web-production-5301.up.railway.app',
    'https://talentscore.vercel.app'

]
CORS_EXPOSE_HEADERS = ["Content-Type", "X-CSRFToken"]

SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SAMESITE = "None"
SESSION_COOKIE_SAMESITE = "None"


USE_X_FORWARDED_HOST = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

SWAGGER_SETTINGS = {
    "SECURITY_DEFINITIONS": {
        "JWT [Bearer {JWT}]": {
            "name": "Authorization",
            "type": "apiKey",
            "in": "header",
        }
    },
    "USE_SESSION_AUTH": False,
}


SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=1),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'ROTATE_REFRESH_TOKENS': False,
    'BLACKLIST_AFTER_ROTATION': False,
    'UPDATE_LAST_LOGIN': False,

    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,
    'VERIFYING_KEY': None,
    'AUDIENCE': None,
    'ISSUER': None,
    'JWK_URL': None,
    'LEEWAY': 0,

    'AUTH_HEADER_TYPES': ('Bearer',),
    'AUTH_HEADER_NAME': 'HTTP_AUTHORIZATION',
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',
    'USER_AUTHENTICATION_RULE': 'rest_framework_simplejwt.authentication.default_user_authentication_rule',

    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
    'TOKEN_TYPE_CLAIM': 'token_type',
    'TOKEN_USER_CLASS': 'rest_framework_simplejwt.models.TokenUser',

    'JTI_CLAIM': 'jti',

    'SLIDING_TOKEN_REFRESH_EXP_CLAIM': 'refresh_exp',
    'SLIDING_TOKEN_LIFETIME': timedelta(minutes=5),
    'SLIDING_TOKEN_REFRESH_LIFETIME': timedelta(days=1),

    # custom
    'AUTH_COOKIE': 'access',
    # Cookie name. Enables cookies if value is set.
    'AUTH_COOKIE_REFRESH': 'refresh',
    # A string like "example.com", or None for standard domain cookie.
    'AUTH_COOKIE_DOMAIN': 'https://talent-score.vercel.app',
    # Whether the auth cookies should be secure (https:// only).
    'AUTH_COOKIE_SECURE': True,
    # Http only cookie flag.It's not fetch by javascript.
    'AUTH_COOKIE_HTTP_ONLY': True,
    'AUTH_COOKIE_PATH': '/',        # The path of the auth cookie.
    # Whether to set the flag restricting cookie leaks on cross-site requests. This can be 'Lax', 'Strict', or None to disable the flag.
    'AUTH_COOKIE_SAMESITE': "None", # TODO: Modify to Lax
}

USE_S3 = True

if USE_S3:
    # aws settings

    AWS_ACCESS_KEY_ID = env("AWS_ACCESS_KEY_ID")
    AWS_SECRET_ACCESS_KEY = env("AWS_SECRET_ACCESS_KEY")
    AWS_STORAGE_BUCKET_NAME = env("AWS_STORAGE_BUCKET_NAME")
    AWS_DEFAULT_ACL = 'public-read'
    AWS_S3_CUSTOM_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com'
    AWS_S3_OBJECT_PARAMETERS = {'CacheControl': 'max-age=86400'}
    # s3 static settings
    AWS_LOCATION = 'static'
    STATIC_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/{AWS_LOCATION}/'
    STATICFILES_STORAGE = 'app.storages.StaticStorage'
    PUBLIC_MEDIA_LOCATION = 'media'
    MEDIA_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/{PUBLIC_MEDIA_LOCATION}/'
    DEFAULT_FILE_STORAGE = 'app.storages.MediaStorage'
else:
    STATIC_URL = '/staticfiles/'
    STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

STATICFILES_DIRS = (os.path.join(BASE_DIR, 'static'),)

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')

