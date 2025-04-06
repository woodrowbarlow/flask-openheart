"""The basic example shows the simplest way to add OpenHeart support to a Flask page."""

from flask import Flask

from flask_openheart import OpenHeartExtension


def create_app():
    """Create a Flask application instance and initialize the OpenHeart extension."""
    app = Flask(__name__)

    openheart = OpenHeartExtension()
    openheart.init_app(app)

    return app


app = create_app()


@app.get("/")
def index():
    """A basic Flask endpoint."""
    return "hello world"
