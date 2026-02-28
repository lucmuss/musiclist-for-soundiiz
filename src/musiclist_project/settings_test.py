"""Django test settings for MusicList Web."""

import musiclist_project.settings as base_settings

for name in dir(base_settings):
    if name.isupper():
        globals()[name] = getattr(base_settings, name)

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

# Use lightweight storages in tests
DEFAULT_FILE_STORAGE = "django.core.files.storage.InMemoryStorage"
STATICFILES_STORAGE = "django.contrib.staticfiles.storage.StaticFilesStorage"

# Debug mode for tests
DEBUG = True

# Secret key for tests
SECRET_KEY = "test-secret-key-not-for-production"
