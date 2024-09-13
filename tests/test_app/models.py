"""Models for the test app."""

from django.db import models


class Foo(models.Model):
    """Simple model."""

    name = models.CharField(max_length=255)

    def __str__(self) -> str:
        return self.name


class Bar(models.Model):
    """A model to test related fields."""

    title = models.CharField(max_length=255)

    foo = models.ForeignKey(Foo, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.title
