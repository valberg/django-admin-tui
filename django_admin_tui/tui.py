"""The core of the Django Admin TUI."""

from __future__ import annotations

from collections import defaultdict
from typing import TYPE_CHECKING

from asgiref.sync import sync_to_async
from django.apps import apps
from django.contrib import admin
from django.contrib.admin.utils import display_for_field
from django.contrib.admin.utils import display_for_value
from django.contrib.admin.utils import label_for_field
from django.contrib.admin.utils import lookup_field
from django.db import models
from textual import log
from textual import on
from textual.app import App
from textual.containers import Container
from textual.widget import Widget
from textual.widgets import Button
from textual.widgets import DataTable
from textual.widgets import Footer
from textual.widgets import Header
from textual.widgets import Label
from textual.widgets import Rule
from textual.widgets import Tree

if TYPE_CHECKING:
    from django.contrib.admin import ModelAdmin
    from django.db.models import Model
    from textual.app import ComposeResult


class DjangoAdminTUI(App):
    """The main TUI application for the Django Admin TUI."""

    def compose(self) -> ComposeResult:
        """Compose the main app."""
        app_dict = defaultdict(list)

        for model, model_admin in admin.site._registry.items():
            app_label = model._meta.app_label

            # get AppConfig instance for the app
            app_config = apps.get_app_config(app_label)

            if app_config.verbose_name:
                app_label = str(app_config.verbose_name).upper()

            model_dict = {
                "model": model,
                "model_admin": model_admin,
            }
            app_dict[app_label].append(model_dict)

        yield RegistryTreeWidget(app_dict=app_dict)

        yield Header(show_clock=True)

        yield Container(id="main")

        yield Footer()

    @on(Tree.NodeSelected)
    @on(Tree.NodeHighlighted)
    async def on_node_selected(self, event: Tree.NodeSelected | Tree.NodeHighlighted) -> None:
        """Handle ."""
        if not event.node.data:
            return
        model = event.node.data["model"]
        model_admin = event.node.data["model_admin"]
        container = self.query_one("#main")
        container.styles.border = "solid", "white"
        container.styles.border_title = model._meta.verbose_name
        await container.remove_children()
        await container.mount(ModelListView(model=model, model_admin=model_admin))


class RegistryTreeWidget(Widget):
    """A widget that displays the registry tree of Django ModelAdmins."""

    DEFAULT_CSS = """
    RegistryTreeWidget {
        dock: left;
        layout: vertical;
        height: auto;
        offset: 0 1;
    }
    """

    def __init__(self, app_dict: dict[str, list[dict[str, Model | ModelAdmin]]]) -> None:
        self.app_dict = app_dict
        super().__init__()

    def compose(self) -> ComposeResult:
        """Compose the widget."""
        tree = Tree("Django Admin")
        tree.show_root = False

        longest_app_label = max(len(app_label) for app_label in self.app_dict)

        self.styles.width = longest_app_label + 5

        # Each app has a label and a list of registered models
        for app_label, model_dicts in self.app_dict.items():
            app_node = tree.root.add(app_label)
            for model_dict in model_dicts:
                app_node.add_leaf(model_dict["model"]._meta.verbose_name_plural.capitalize(), data=model_dict)

        tree.root.expand_all()
        yield tree


class ModelListView(Widget):
    """A widget that displays a list of objects for a Django model.

    This is the equivalent of the Django admins changelist view.
    """

    DEFAULT_CSS = """
    ListView {
        layout: vertical;
        height: auto;
        border: solid white;
    }
    """

    model_admin: ModelAdmin
    model: Model

    def __init__(self, *, model_admin: ModelAdmin, model: Model) -> None:
        self.model_admin = model_admin
        self.model = model
        super().__init__()

    def compose(self) -> ComposeResult:
        """Compose the widget."""
        self.border_title = self.model.__name__

        yield Label(f"Select {self.model._meta.verbose_name} to change")

        # Add button to add a new object
        yield Button("Add", id="add_button")

        yield Rule()

        # Create a data table
        yield DataTable(cursor_type="row")

    async def on_mount(self) -> None:
        """Handle the mount event."""
        table = self.query_one(DataTable)

        columns = []

        for field_name in self.model_admin.list_display:
            text, attr = label_for_field(field_name, self.model, model_admin=self.model_admin, return_attr=True)
            columns.append(str(text))

        log(f"Columns: {columns}")

        table.add_columns(*columns)

        async for obj in self.model.objects.all():
            empty_value_display = self.model_admin.get_empty_value_display()
            row = []

            for field_name in self.model_admin.list_display:
                f, attr, value = await sync_to_async(
                    lookup_field,
                )(field_name, obj, self.model_admin)
                empty_value_display = getattr(attr, "empty_value_display", empty_value_display)
                log(f"Field: {f}, Attr: {attr}, Value: {value}")
                if f is None or f.auto_created:
                    boolean = getattr(attr, "boolean", False)
                    # Set boolean for attr that is a property, if defined.
                    if isinstance(attr, property) and hasattr(attr, "fget"):
                        boolean = getattr(attr.fget, "boolean", False)
                    result_repr = display_for_value(value, empty_value_display, boolean)
                elif isinstance(f.remote_field, models.ManyToOneRel):
                    field_val = getattr(obj, f.name)
                    result_repr = empty_value_display if field_val is None else field_val
                else:
                    result_repr = display_for_field(value, f, empty_value_display)

                row.append(result_repr)
            log(f"Row: {row}")
            table.add_row(*row)
