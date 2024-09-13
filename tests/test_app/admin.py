"""Admin for the test app."""

from django.contrib import admin
from test_app.models import Bar
from test_app.models import Foo


@admin.register(Foo)
class FooAdmin(admin.ModelAdmin):
    """Admin for the Foo model."""


@admin.register(Bar)
class BarAdmin(admin.ModelAdmin):
    """Admin for the Bar model."""

    list_display = ("title", "foo__name")
