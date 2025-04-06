"""A Flask extension to add support for OpenHeart protocol."""

from flask import Blueprint

DEFAULT_URL_PREFIX = "/openheart"


blueprint = Blueprint("openheart", __name__)


@blueprint.get("/<path:subpath>")
def get_reactions(subpath):
    """TODO."""
    return f"path: {subpath}"


class OpenHeart:
    """A simple protocol for allowing emoji-based reactions to URIs."""


class OpenHeartExtension:
    """A Flask extension to add support for OpenHeart protocol."""

    def __init__(self, app=None):
        """A Flask extension to add support for OpenHeart protocol.

        Args:
            app: (optional) The Flask application instance. If supplied, the extension will be initialized immediately.
            Otherwise it must be initialized later via `init_app`.
        """
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        """Initialize the OpenHeart extension with a Flask application instance.

        Args:
            app: The Flask application instance.

        Raises:
            RuntimeError: The extension is already initialized.
        """
        if "openheart" in app.extensions:
            msg = "OpenHeart is already initialized"
            raise RuntimeError(msg)
        app.extensions["openheart"] = self
        url_prefix = DEFAULT_URL_PREFIX
        if "OPENHEART_URL_PREFIX" in app.config:
            url_prefix = app.config["OPENHEART_URL_PREFIX"]
        app.register_blueprint(blueprint, url_prefix=url_prefix)
        app.openheart = OpenHeart()
