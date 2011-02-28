DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'cloudmailin.db',
    },
}

INSTALLED_APPS = (
    'cloudmailin.tests',
)

ROOT_URLCONF = 'cloudmailin.tests.urls'