DEBUG = True
ALLOWED_HOSTS = ['testserver', '127.0.0.1', 'localhost', '::1']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'quack_db',
        'USER': 'quack',
        'PASSWORD': 'Not_a_duck.',
        'HOST': '127.0.0.1',
#        'NAME': 'postgres',
 #       'USER': 'postgres',
  #      'HOST': 'database',
        'PORT': '5432',
    }
}
