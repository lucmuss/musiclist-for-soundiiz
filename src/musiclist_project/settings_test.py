"""Django test settings for MusicList Web."""

from .settings import *

# Use SQLite for tests
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": ":memory:",
    }
}

# Disable password hashing for faster tests
PASSWORD_HASHERS = [
    "django.contrib.auth.hashers.MD5PasswordHasher",
]

# Disable Celery for tests
CELERY_TASK_ALWAYS_EAGER = True

# Use in-memory file storage
DEFAULT_FILE_STORAGE = "django.core.files.storage.InMemoryStorage"

# Debug mode for tests
DEBUG = True

# Secret key for tests
SECRET_KEY = "test-secret-key-not-for-production"
