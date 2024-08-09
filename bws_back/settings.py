"""
Django settings for bws_back project.

Generated by 'django-admin startproject' using Django 5.0.6.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""
from datetime import timedelta
import os
from pathlib import Path
import sqlalchemy as db
from sqlalchemy.orm import scoped_session, sessionmaker

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-j=5))xznqn@)#_b)k3-r$0k&ozss5dwm!5ee-sk_9)dol-4s4p'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.BasicAuthentication',
    ]
}


SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60),  # Tempo de vida do token de acesso
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),     # Tempo de vida do token de refresh
    'ROTATE_REFRESH_TOKENS': True,                   # Rotaciona o token de refresh ao usá-lo
    'BLACKLIST_AFTER_ROTATION': True,                # Blacklist do refresh token antigo
    'ALGORITHM': 'HS256',
    'SIGNING_KEY': 'your-signing-key',
    'AUTH_HEADER_TYPES': ('Bearer',),
}
# Application definition

SHARED_APPS = (
    'django_tenants',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'core',
    'core.customers'
)

TENANT_APPS = ('restaurant',
               'core.configuracao',
               'core.usuario',
               'core.usuario.cliente',
               'core.usuario.funcionario',
               'core.produto',
               'core.pedido',
               'core.carrinho'
               )

INSTALLED_APPS = list(SHARED_APPS) + [app for app in TENANT_APPS if app not in SHARED_APPS]
MIDDLEWARE = [
    'core.middleware.GlobalRequestMiddleware',
    #'core.middleware.JWTAuthenticationMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django_tenants.middleware.main.TenantMainMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'bws_back.urls'

AUTH_USER_MODEL = 'usuario.User'

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
            ],
        },
    },
]

WSGI_APPLICATION = 'bws_back.wsgi.application'

TENANT_MODEL = "customers.Conta"

TENANT_DOMAIN_MODEL = "customers.Dominio"
# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    'default': {
        # Engine do django tenants
        'ENGINE': 'django_tenants.postgresql_backend',
        'NAME': os.getenv('DATABASE_NAME', 'postgres'),
        'USER': os.getenv('DATABASE_USER', 'postgres.hvonjldepqkbghjlcsjl'),
        'PASSWORD': os.getenv('DATABASE_PASSWORD', '20uPdNbY0cd0K8ub'),
        'HOST': os.getenv('DATABASE_HOST', 'aws-0-sa-east-1.pooler.supabase.com'),
        'PORT': os.getenv('DATABASE_PORT', '6543'),
        'OPTIONS': {'application_name': 'BWS - Core'},
    }
}

DB_CONNECTIONS = {
    'default': {
        'user': DATABASES['default']['USER'],
        'password': DATABASES['default']['PASSWORD'],
        'host': DATABASES['default']['HOST'],
        'port': DATABASES['default']['PORT'],
        'name': DATABASES['default']['NAME'],
        'url': f"postgresql+psycopg2://"
        f"{DATABASES['default']['USER']}:"
        f"{DATABASES['default']['PASSWORD']}@"
        f"{DATABASES['default']['HOST']}/"
        f"{DATABASES['default']['NAME']}?client_encoding=latin1",
    }
}


DB_CONNECTIONS['default']['engine'] = db.create_engine(
    DB_CONNECTIONS['default']['url'],
    pool_size=10,
    max_overflow=0,
    # https://docs.sqlalchemy.org/en/20/core/pooling.html#dealing-with-disconnects
    pool_pre_ping=True
    # DESCONMENTE SE QUISER VER AS QUERYS EXECUTADAS
    # ,
    # echo_pool="debug",
    # echo=True,
    ,
    pool_timeout=30,
)
# ABRE O POOL DE CONEXAO
with DB_CONNECTIONS['default']['engine'].connect() as conn:
    conn.execute(db.text('select 1'))

DB_CONNECTIONS['default']['conexao'] = None

DB_CONNECTIONS['default']['sessoes'] = scoped_session(sessionmaker(bind=DB_CONNECTIONS['default']['engine']))
DATABASE_ROUTERS = ('django_tenants.routers.TenantSyncRouter',)
# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
