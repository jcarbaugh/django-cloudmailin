DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'cloudmailin.db',
    },
}

INSTALLED_APPS = (
    'cloudmailin',
)

ROOT_URLCONF = 'cloudmailin.test.urls'