"""Django settings for tests."""

from __future__ import annotations

import os
from pathlib import Path
from typing import Any

ALLOWED_HOSTS: list[str] = []

BASE_DIR = Path(__file__).resolve().parent

DEBUG_ENV = os.environ.get("DEBUG")
DEBUG = True

DATABASE_NAME = BASE_DIR / "db.sqlite3"

DATABASES: dict[str, dict[str, Any]] = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": DATABASE_NAME,
    },
}

INSTALLED_APPS = [
    # Third Party
    "django_admin_tui",
    # Contrib
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.sessions",
    "django.contrib.contenttypes",
    "django.contrib.staticfiles",
    "django.contrib.messages",
    # Local
    "test_app",
]

MIDDLEWARE: list[str] = [
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
]

ROOT_URLCONF = "urls"

SECRET_KEY = "NOTASECRET"  # noqa: S105

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "APP_DIRS": True,
        "DIRS": [BASE_DIR / "templates" / "django"],
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ]
        },
    },
]

USE_TZ = True

STATICFILES_DIRS = [
    BASE_DIR / "static",
]

STATIC_URL = "/static/"
