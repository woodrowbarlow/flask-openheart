"""A Flask application which bundles all example applications into one.

Note: This file is not a Flask-OpenHeart example; it is just a convenient way of serving all examples at once.
"""

import importlib
from pathlib import Path

from flask import Flask
from werkzeug.middleware.dispatcher import DispatcherMiddleware


def _discover_modules(parent_dir):
    for entry in parent_dir.iterdir():
        if not entry.is_dir():
            continue
        if entry.name.startswith("."):
            continue
        if entry.name.startswith("_"):
            continue
        if not (entry / "__init__.py").is_file():
            continue
        yield entry.name, importlib.import_module(f"{parent_dir.name}.{entry.name}")


class ExamplesMiddleware(Flask):
    """A middleware application which hosts all example apps under sub-paths."""

    def __init__(self, *args, **kwargs):
        """Create a new instancle of the examples middleware app."""
        examples_dir = Path(__file__).resolve().parent
        self.examples = [
            {
                "path": f"/{name}",
                "name": module.__name__,
                "description": module.__doc__,
                "app": module.app,
            }
            for name, module in _discover_modules(examples_dir)
        ]

        super().__init__(*args, **kwargs)
        self.wsgi_app = DispatcherMiddleware(
            self.wsgi_app, {example["path"]: example["app"] for example in self.examples}
        )


app = ExamplesMiddleware(__name__)


@app.get("/")
def index():
    """A default endpoint which generates links to each specific example."""

    def render_example(example):
        return f'<li><a href="{example["path"]}" title="{example["description"]}">{example["name"]}</a></li>'

    def render_examples():
        return f"<ul>{''.join([render_example(example) for example in app.examples])}</ul>"

    return "<h1>Examples</h1>" + render_examples()
