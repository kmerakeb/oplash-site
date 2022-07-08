from pathlib import Path

from decouple import config
import os

BASE_DIR = Path(__file__).resolve().parent.parent.parent


# ==============================================================================
# CORE SETTINGS
# ==============================================================================

SECRET_KEY = config(
    "SECRET_KEY", default="django-insecure$realworld.config.settings.local"
)

DEBUG = config("DEBUG", default=False, cast=bool)

ALLOWED_HOSTS = ["127.0.0.1", "localhost", "oplash.com"]

INSTALLED_APPS = [
    # Django apps
    'filebrowser',
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    'django.contrib.sites',
    
     
    # 3rd party libraries
    'django_comments',
    "taggit",
    "widget_tweaks",
    # Local apps
    "oplash.apps.accounts",
    "oplash.apps.articles",
    "oplash.apps.comments",
    'tinymce',
]

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

ROOT_URLCONF = "oplash.config.urls"

WSGI_APPLICATION = "oplash.config.wsgi.application"


# ==============================================================================
# MIDDLEWARE SETTINGS
# ==============================================================================

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

X_FRAME_OPTIONS = 'SAMEORIGIN'

# ==============================================================================
# TEMPLATES SETTINGS
# ==============================================================================

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
           # "debug": DEBUG,
        },
    },
]


# ==============================================================================
# DATABASES SETTINGS
# ==============================================================================

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR.parent / "db.sqlite3",
    }
}


# ==============================================================================
# AUTHENTICATION AND AUTHORIZATION SETTINGS
# ==============================================================================

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

AUTH_USER_MODEL = "accounts.User"

ADMIN_URL = config("ADMIN_URL", default="admin/")

LOGIN_URL = "/login/"

LOGIN_REDIRECT_URL = "/"


# ==============================================================================
# I18N AND L10N SETTINGS
# ==============================================================================

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True

# ==============================================================================
# FILE BROWSER SETTINGS
# ==============================================================================

FILEBROWSER_DIRECTORY = ''
DIRECTORY = ''
# ==============================================================================
# TINYMCE SETTINGS
# ==============================================================================

DEFAULT = {
    'selector': 'textarea',
    'theme': 'modern',
     'plugins': "preview",
  'menubar': "view",
  'toolbar': "preview",
    'plugins': 'link image preview codesample contextmenu table code lists emoticons',
    'toolbar1': 'formatselect | bold italic underline | alignleft aligncenter alignright alignjustify '
               '| bullist numlist | outdent indent | table | link image | codesample | preview code | emoticons',
    'contextmenu': 'formats | link image',
    'menubar': True,
    'inline': True,
    'statusbar': True,
   
}

TINYMCE_DEFAULT_CONFIG = {
    

  'plugins': "toolstable preview link image preview codesample contextmenu table code lists image lists code pagebreak emoticons media  mediaembed codesample anchor image imagetools insertdatetime link hr textcolor visualblocks nonbreaking fullscreen",
  'menubar': 'view tools table codesample imagetools insert',

  'toolbar': "formatselect | bold italic underline | alignleft aligncenter alignright alignjustify lists numlist bullist code tools emoticons  preview image media  mediaembed pagebreak table codesample anchor insertdatetime link hr forecolor backcolor visualblocks nonbreaking fullscreen" ,
  'content_css': 'https://maxcdn.bootstrapcdn.com/bootstrap/3.3.6/css/bootstrap.min.css',
   'width': 'auto',
    'height': 500,
    
}

# ==============================================================================
# STATIC FILES SETTINGS
# ==============================================================================

STATICFILES_DIRS = [BASE_DIR / "static"]

STATIC_URL = "/static/"

STATIC_ROOT = BASE_DIR / "staticfiles"

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media_root"


'''STATIC_URL = '/static/'
MEDIA_URL = '/media/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static_in_env')]
VENV_PATH = os.path.dirname(BASE_DIR)
STATIC_ROOT = os.path.join(VENV_PATH, 'static_root')
MEDIA_ROOT = os.path.join(VENV_PATH, 'media_root')'''

SITE_ID = 7