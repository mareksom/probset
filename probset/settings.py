"""
Django settings for probset project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '+x=df)-#r(ub3jc=vlzv)41kli7-5lq_404n#)l%xnl#3&2vm9'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = ['wic2014-probset.staszic.waw.pl',
                 'probset.staszic.waw.pl']

WSGI_APPLICATION = 'probset.wsgi.application'


# Application definition

INSTALLED_APPS = (
	'django.contrib.admin',
	'django.contrib.auth',
	'django.contrib.contenttypes',
	'django.contrib.sessions',
	'django.contrib.messages',
	'django.contrib.staticfiles',
	'mytemplates',
	'accounts',
	'news',
	'help',
	'tags',
	'problems',
	'packages',
	'contests',
	'threads',
	'forum',
	'impersonate',
)

MIDDLEWARE = [
	'django.contrib.sessions.middleware.SessionMiddleware',
	'django.middleware.common.CommonMiddleware',
	'django.middleware.csrf.CsrfViewMiddleware',
	'django.contrib.auth.middleware.AuthenticationMiddleware',
	'django.contrib.messages.middleware.MessageMiddleware',
	'django.middleware.clickjacking.XFrameOptionsMiddleware',
	'impersonate.middleware.ImpersonateMiddleware',
]

ROOT_URLCONF = 'probset.urls'

WSGI_APPLICATION = 'probset.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
	'default': {
		'ENGINE': 'django.db.backends.sqlite3',
		'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
	}
}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en'

TIME_ZONE = 'Europe/Warsaw'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = 'static/'

STATICFILES_DIRS = [
	os.path.join(BASE_DIR, 'probset-static')
]

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'templates'),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                # zmigrowane TEMPLATE_CONTEXT_PROCESSORS
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.request',
                'probset.context_processors.messages',
                'probset.context_processors.kasia',
                'probset.context_processors.forum_posts',
                'probset.context_processors.comments_posts',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# Media files

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

IMPERSONATE = {
	'REDIRECT_URL': '/',
}
