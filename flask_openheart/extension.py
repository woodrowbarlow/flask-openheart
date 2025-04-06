"""A Flask extension to add support for OpenHeart protocol."""

from flask import abort, current_app, jsonify, request

from flask_openheart.openheart import InvalidReactionError, OpenHeart

DEFAULT_GLOBAL_ENABLE = False
DEFAULT_URL_PREFIX = "/openheart"
DEFAULT_DATABASE_URI = "file:openheart.db"
DEFAULT_DATABASE_PREFIX = "openheart"


def oh_endpoint(**kwargs):
    """The endpoint for all OpenHeart API calls.

    Returns:
        The up-to-date reactions, in JSON format.
    """
    endpoint = request.endpoint.removeprefix("openheart.")
    slug = current_app.slug_for(endpoint, **kwargs)
    openheart = current_app.openheart
    if request.method == "POST":
        data = request.get_data(as_text=True)
        try:
            return jsonify(openheart.react(slug, data))
        except InvalidReactionError as e:
            abort(418, description=str(e))
    return jsonify(openheart.reactions(slug))


class OpenHeartExtension:
    """A Flask extension to add support for OpenHeart protocol."""

    def __init__(self, app=None, **options):
        """A Flask extension to add support for OpenHeart protocol.

        Args:
            app: (optional) The Flask application instance. If supplied, the extension will be initialized immediately.
            Otherwise it must be initialized later via `init_app`.
            options: (optional) Additional options to pass to `init_app`.
        """
        if app is not None:
            self.init_app(app, **options)

    def slug_for(self, endpoint, **args):  # noqa: ARG002
        """Like `url_for` except this returns a unique slug for the object represented.

        Args:
            endpoint: the endpoint name.
            args: additional arguments.

        Returns:
            a unique slug
        """
        # TODO: allow user to override
        return endpoint

    def init_app(self, app, **options):
        """Initialize the OpenHeart extension with a Flask application instance.

        Args:
            app: The Flask application instance.
            options: (optional) Configuration overrides.

        Raises:
            RuntimeError: The extension is already initialized.
        """
        if "openheart" in app.extensions:
            msg = "OpenHeart is already initialized"
            raise RuntimeError(msg)
        app.extensions["openheart"] = self
        global_enable = options.get("global_enable", app.config.get("OPENHEART_GLOBAL_ENABLE", DEFAULT_GLOBAL_ENABLE))
        url_prefix = options.get("url_prefix", app.config.get("OPENHEART_URL_PREFIX", DEFAULT_URL_PREFIX))
        database_uri = options.get("database_uri", app.config.get("OPENHEART_DATABASE_URI", DEFAULT_DATABASE_URI))
        database_prefix = options.get(
            "database_prefix", app.config.get("OPENHEART_DATABASE_PREFIX", DEFAULT_DATABASE_PREFIX)
        )

        def route(rule, **options):
            def decorator(f):
                # TODO should we call the original route function instead of directly calling add_url_rule?
                oh_enabled = options.pop("openheart", global_enable)
                endpoint = options.pop("endpoint", None)
                if endpoint is None:
                    endpoint = f.__name__
                app.add_url_rule(rule, endpoint, f, **options)
                if oh_enabled:
                    options.update({"methods": ["GET", "POST"]})
                    endpoint = f"openheart.{endpoint}"
                    oh_rule = url_prefix + rule
                    app.add_url_rule(oh_rule, endpoint, oh_endpoint, **options)
                return f

            return decorator

        app.openheart = OpenHeart(database_uri, database_prefix)
        app.route = route
        app.slug_for = self.slug_for
