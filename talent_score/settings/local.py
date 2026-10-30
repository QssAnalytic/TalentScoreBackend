from pathlib import Path
from datetime import timedelta
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }

import os as _os

# SQLITE_PATH points at the persistent volume in production (e.g. /data/db.sqlite3),
# so redeploys keep users and reports. scripts/prepare_data.py seeds it from db2.sqlite3 once.
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': _os.environ.get('SQLITE_PATH', str(BASE_DIR / 'db2.sqlite3')),
    }
}


import os

# Use Redis when REDIS_URL is set (e.g. a Railway Redis service); otherwise an in-process cache.
if os.environ.get("REDIS_URL"):
    CACHES = {
        "default": {
            "BACKEND": "django.core.cache.backends.redis.RedisCache",
            "LOCATION": os.environ["REDIS_URL"],
        }
    }
else:
    CACHES = {"default": {"BACKEND": "django.core.cache.backends.locmem.LocMemCache"}}


