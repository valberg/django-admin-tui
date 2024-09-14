# django-admin-tui

[![PyPI - Version](https://img.shields.io/pypi/v/django-admin-tui.svg)](https://pypi.org/project/django-admin-tui)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/django-admin-tui.svg)](https://pypi.org/project/django-admin-tui)

-----

**Table of Contents**

- [About](#about)
- [Installation](#installation)
- [Usage](#usage)
- [License](#license)
- [Inspiration](#inspiration)

## About

`django-admin-tui` is a project aiming to render the Django admin in a text-based user interface (TUI)
using [Textual](https://textual.textualize.io/), bringing one of Djangos killer features to a terminal near you.

## Installation and setup

```console
pip install django-admin-tui
```

Then add `django_admin_tui` to your `INSTALLED_APPS`.

## Usage

Simply run `./manage.py admin_tui` and see all your registered admins right there in your terminal.

## License

`django-admin-tui` is distributed under the terms of the [MIT](https://spdx.org/licenses/MIT.html) license.

## Inspiration 

Besides the Django admin and textual, [http://github.com/anze3db/django-tui](http://github.com/anze3db/django-tui) was the whole reason for the idea of this project.