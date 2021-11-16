"""
Django settings for featuringeg_data project.

Generated by 'django-admin startproject' using Django 3.2.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""

from pathlib import Path
from elasticsearch import RequestsHttpConnection

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-4r^9d)%it*cwm%(42y7tihz9^2m6m=1kmq%=r%%zyppyk4l1sd'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'instagram_crawler',
    'tiktok_crawler',
    'xiaohongshu_crawler',
    'youtube_crawler',
    'django_elasticsearch_dsl',
    'rest_framework',
    'drf_generators',
    'drf_yasg',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'featuringeg_data.urls'

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

WSGI_APPLICATION = 'featuringeg_data.wsgi.application'


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

LANGUAGE_CODE = 'ko-KR'

TIME_ZONE = 'Asia/Seoul'
USE_I18N = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = '/static/'

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'



# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases


DATABASE_ROUTERS = [
    'featuringeg_data.router.FeaturingEngineRouter',
]


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'featuringscore',
        'USER': 'poza',
        'PASSWORD': 'Admin1992!db',
        'HOST': 'featuringscore.cbamritymyix.ap-northeast-2.rds.amazonaws.com',
        'PORT': '5432',
    },
    'score_crawler_writer' : {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'featuringscore-crawler',
        'USER': 'poza',
        'PASSWORD': 'Admin1992!db',
        'HOST': 'featuringscore-crawler-migrated-cluster.cluster-cbamritymyix.ap-northeast-2.rds.amazonaws.com',
        'PORT': '5432',
    },
    'score_crawler_read' : {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'featuringscore-crawler',
        'USER': 'poza',
        'PASSWORD': 'Admin1992!db',
        'HOST': 'featuringscore-crawler-migrated-cluster.cluster-ro-cbamritymyix.ap-northeast-2.rds.amazonaws.com',
        'PORT': '5432',
    },
    'score_crawler_youtube_writer' : {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'featuringscore-crawler-youtube',
        'USER': 'poza',
        'PASSWORD': 'Admin1992!db',
        'HOST': 'featuringscore-crawler-youtube.cluster-cbamritymyix.ap-northeast-2.rds.amazonaws.com',
        'PORT': '5432',
    },
    'score_crawler_youtube_read' : {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'featuringscore-crawler-youtube',
        'USER': 'poza',
        'PASSWORD': 'Admin1992!db',
        'HOST': 'featuringscore-crawler-youtube.cluster-ro-cbamritymyix.ap-northeast-2.rds.amazonaws.com',
        'PORT': '5432',
    },
    'score_crawler_tiktok' : {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'featuringscore-crawler-tiktok',
        'USER': 'poza',
        'PASSWORD': 'Admin1992!db',
        'HOST': 'featuringscore-crawler-tiktok.cbamritymyix.ap-northeast-2.rds.amazonaws.com',
        'PORT': '5432',
    },
    'score_xiaohongshu' : {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'featuring',
        'USER': 'poza',
        'PASSWORD': 'Admin1992!db',
        'HOST': 'featuring-xiaohongshu.cbamritymyix.ap-northeast-2.rds.amazonaws.com',
        'PORT': '3306',
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
            'charset': 'utf8mb4',
        }
    },
}

ELASTICSEARCH_DSL={
    'default': {
        'hosts': 'https://vpc-featuring-instagram-gv474znuicbypbtgd2pzi4loce.ap-northeast-2.es.amazonaws.com',
        'http_auth': ('admin', 'Admin1992@'),
        'port': 443,
        'use_ssl': True,
        'verify_certs': True,
        'connection_class': RequestsHttpConnection,
    },
}


## drf-generators
REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 30
}