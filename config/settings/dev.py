from .base import *  # noqa: F403


CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
        "LOCATION": "",
    },
}

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
