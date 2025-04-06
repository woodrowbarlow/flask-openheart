"""A Flask application which bundles all example applications into one."""

import importlib
from pathlib import Path

from flask import Flask
from werkzeug.middleware.dispatcher import DispatcherMiddleware


def discover_examples():
    """Automatically discover and mount all example sub-apps."""
    path = Path(__file__).resolve().parent
    for entry in path.iterdir():
        if not entry.is_dir():
            continue
        if entry.name.startswith("."):
            continue
        if entry.name.startswith("_"):
            continue
        module = importlib.import_module(f"examples.{entry.name}")
        yield {
            "path": f"/{entry.name}",
            "name": module.__name__,
            "description": module.__doc__,
            "app": module.app,
        }


app = Flask(__name__)
examples = list(discover_examples())
app.wsgi_app = DispatcherMiddleware(app.wsgi_app, {example["path"]: example["app"] for example in examples})


@app.get("/")
def index():
    """A default endpoint which generates links to each specific example."""

    def render_example(example):
        return f'<li><a href="{example["path"]}" title="{example["description"]}">{example["name"]}</a></li>'

    def render_examples():
        return f"<ul>{''.join([render_example(example) for example in examples])}</ul>"

    return "<h1>Examples</h1>" + render_examples()
