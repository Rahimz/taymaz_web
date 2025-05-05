from .base import *


SECRET_KEY = pro_secret_key

DEBUG = False

ALLOWED_HOSTS = ['negar-taymaz.ir', 'www.negar-taymaz.ir']

CSRF_TRUSTED_ORIGINS = [
    'https://negar-taymaz.ir',
    'https://www.negar-taymaz.ir',
]