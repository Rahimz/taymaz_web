from .base import *


SECRET_KEY = pro_secret_key

DEBUG = False

ALLOWED_HOSTS = ['negar-taymaz.ir', 'www.negar-taymaz.ir']

CSRF_TRUSTED_ORIGINS = [
    'https://negar-taymaz.ir',
    'https://www.negar-taymaz.ir',
]

# Allow files up to 2 GB
DATA_UPLOAD_MAX_MEMORY_SIZE = 2 * 1024 * 1024 * 1024  # 2 GB
FILE_UPLOAD_MAX_MEMORY_SIZE = 2 * 1024 * 1024 * 1024  # 2 GB