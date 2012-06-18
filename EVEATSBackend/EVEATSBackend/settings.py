# Django settings for EVEATS project.

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
  # ('Your Name', 'your_email@example.com'),
)

MANAGERS = ADMINS

DATABASES = {
  'default': {
    'ENGINE'    : 	'django.db.backends.mysql', 	# Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
    'NAME'      : 	'c0_eveats',                  # Or path to database file if using sqlite3.
    'USER'      : 	'c0_eveats',                  # Not used with sqlite3.
    'PASSWORD'  :   'eveats',	                    # Not used with sqlite3.
    'HOST'      : 	'localhost',                	# Set to empty string for localhost. Not used with sqlite3.
    'PORT'      : 	'3306',                     	# Set to empty string for default. Not used with sqlite3.
    'OPTIONS': {
      'init_command': 'SET storage_engine=INNODB;',
    }
  },
}

# EVE API Connection URL 
EVE_API_HOST = "api.eveonline.com"
EVE_API_PORT = 443

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'Europe/Berlin'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale
USE_L10N = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = ''

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = ''

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = ''

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/EVEATS/'

# Additional locations of static files
STATICFILES_DIRS = (
  # Put strings here, like "/home/html/static" or "C:/www/django/static".
  # Always use forward slashes, even on Windows.
  # Don't forget to use absolute paths, not relative paths.
  "/home/christian/Workspace/EVEATS/EVEATSFrontend/",
  "/home/wilhelm/EVEATS/EVEATSFrontend",
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
  'django.contrib.staticfiles.finders.FileSystemFinder',
  'django.contrib.staticfiles.finders.AppDirectoriesFinder',
  #'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = '&z&8)!e@twh=hc*76ng$fnikm+z+*94a=-m2l*b^l&&p_#y8d8'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
  'django.template.loaders.filesystem.Loader',
  'django.template.loaders.app_directories.Loader',
  'django.template.loaders.eggs.Loader',
)

# Cache backend memcached
CACHES = {
  'default': {
    'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
    'LOCATION': '127.0.0.1:11211',
    'KEY_PREFIX': 'eveatsdev'
  }
}

# Celery : Distributed Task Queue
import djcelery
djcelery.setup_loader()

BROKER_HOST                   = "localhost"
BROKER_PORT                   = 5672
BROKER_USER                   = "eveats"
BROKER_PASSWORD               = "eveats"
BROKER_VHOST                  = "eveatsdev"

CELERYD_CONCURRENCY           = 64
CELERYD_PREFETCH_MULTIPLIER   = 1
CELERYD_LOG_LEVEL             = "INFO"
CELERYBEAT_LOG_LEVEL          = "INFO"

# Django Middelware Classes
MIDDLEWARE_CLASSES = (
  'django.middleware.common.CommonMiddleware',
  'django.contrib.sessions.middleware.SessionMiddleware',
  'django.middleware.csrf.CsrfViewMiddleware',
  'django.contrib.auth.middleware.AuthenticationMiddleware',
  #'django.contrib.messages.middleware.MessageMiddleware',
  #'django.middleware.cache.UpdateCacheMiddleware',
  #'django.middleware.cache.FetchFromCacheMiddleware',
)

AUTHENTICATION_BACKENDS = (
  'django.contrib.auth.backends.ModelBackend',
  'permission.backends.RoleBackend',
  'permission.backends.PermissionBackend',
)

ROOT_URLCONF = 'EVEATSBackend.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'EVEATSBackend.wsgi.application'

TEMPLATE_DIRS = (
  # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
  # Always use forward slashes, even on Windows.
  # Don't forget to use absolute paths, not relative paths.
  #"/usr/local/lib/python2.6/dist-packages/django_extensions/templates",
  #"/usr/local/lib/python2.6/dist-packages/django_extensions/templates/django_extensions/graph_models",
)

INSTALLED_APPS = (
  'evedb',
  'eve',
  'accounts',
  'common',
  'evecentral',
  'djcelery',
  'permission',
  'django.contrib.auth',
  'django.contrib.contenttypes',
  'django.contrib.sessions',
  'django.contrib.staticfiles',
  'django_extensions',
  #'django.contrib.sites',
  #'django.contrib.messages',
  # Uncomment the next line to enable the admin:
  # 'django.contrib.admin',
  # Uncomment the next line to enable admin documentation:
  # 'django.contrib.admindocs',
)

LOGGING = {
  'version': 1,
  'disable_existing_loggers': True,
  'formatters': {
    'verbose': {
      'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
    },
    'simple': {
      'format': '[%(levelname)s] %(name)s: %(message)s'
    },
  },
  'handlers': {
    'default': {
      'level':'DEBUG',
      'class':'logging.handlers.RotatingFileHandler',
      'filename': 'logs/default.log',
      'maxBytes': 1024*1024*5, # 5 MB
      'backupCount': 7,
      'formatter':'verbose',
    },  
    'requests': {
      'level':'DEBUG',
      'class':'logging.handlers.RotatingFileHandler',
      'filename': 'logs/request.log',
      'maxBytes': 1024*1024*5, # 5 MB
      'backupCount': 7,
      'formatter':'verbose',
    },
    'db': {
      'level':'INFO',
      'class':'logging.handlers.RotatingFileHandler',
      'filename': 'logs/db.log',
      'maxBytes': 1024*1024*5, # 5 MB
      'backupCount': 7,
      'formatter':'verbose',
    },
  },
  'loggers': {
    '': {
      'handlers': ['default'],
      'level': 'DEBUG',
      'propagate': True
    },
    'django.request': {
      'handlers': ['requests'],
      'level': 'DEBUG',
      'propagate': False
    },
    'django.db.backends': {
      'handlers': ['db'],
      'level': 'DEBUG',
      'propagate': False
    },
  }
}

