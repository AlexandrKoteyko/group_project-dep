from .settings import *

# Використовуємо SQLite для розробки
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

DEBUG = True
ALLOWED_HOSTS = ['localhost', '127.0.0.1']

# Вимикаємо WhiteNoise для розробки
MIDDLEWARE = [m for m in MIDDLEWARE if m != 'whitenoise.middleware.WhiteNoiseMiddleware']