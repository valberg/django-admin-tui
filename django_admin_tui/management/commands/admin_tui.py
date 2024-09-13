"""Management command to run the Django Admin TUI."""

from typing import Any

from django.core.management import BaseCommand

from django_admin_tui.tui import DjangoAdminTUI


class Command(BaseCommand):
    """Management command to run the Django Admin TUI."""

    help = """Run a TUI to browse django models."""

    def handle(self, *args: Any, **options: Any) -> None:  # noqa: ARG002, ANN401
        """Handle the management command."""
        app = DjangoAdminTUI()
        app.run()
