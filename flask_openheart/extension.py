"""A Flask extension to add support for OpenHeart protocol."""

from functools import wraps

from flask import current_app, jsonify, request

from flask_openheart.config import OpenHeartConfig
from flask_openheart.controller import OpenHeartController, OpenHeartRequestController


def before_request():
    """If the request is for an OpenHeart-enabled endpoint, inject OpenHeart data about the request."""
    enabled = current_app.openheart.is_enabled_for(request.endpoint, **request.view_args)
    if enabled:
        request.openheart = OpenHeartRequestController(request.endpoint, **request.view_args)
    else:
        request.openheart = None


def handler(**args):
    """The Flask endpoint handler for all OpenHeart requests."""
    endpoint = request.endpoint.removeprefix(f"openheart.{request.method.lower()}.")
    if request.method == "POST":
        data = request.get_data(as_text=True)
        reactions = current_app.openheart.react_to(data, endpoint, **args)
    else:
        reactions = current_app.openheart.reactions_for(endpoint, **args)
    return jsonify(reactions)


def _get_options(options, config):
    value = options.pop("openheart", None)
    if value is None:
        return False, OpenHeartConfig(**config)
    if isinstance(value, bool):
        return value, OpenHeartConfig(**config)
    opts = config.copy()
    opts.update(value)
    return True, OpenHeartConfig(**opts)


def _adapt_rule(config, method, rule, endpoint, **options):
    options.update({"methods": [method.upper()]})
    prefix = config.url_prefix
    if method.upper() == "POST":
        prefix = config.post_url_prefix
    return f"{prefix}{rule}", f"openheart.{method.lower()}.{endpoint}", options


class OpenHeart:
    """A Flask extension to add support for OpenHeart protocol."""

    def __init__(self, app=None, **options):
        """A Flask extension to add support for OpenHeart protocol.

        :param app: (optional) The Flask application instance. If supplied, the extension will be initialized
            immediately. Otherwise it must be initialized later via `init_app`.
        :param options: (optional) Additional options to pass to `init_app`.
        """
        if app is not None:
            self.init_app(app, **options)

    def init_app(self, app, **options):
        """Initialize the OpenHeart extension with a Flask application instance.

        :param app: The Flask application instance.
        :param options: (optional) Configuration overrides.
        """
        config = {
            key.remove_prefix("OPENHEART_").lower(): value
            for key, value in app.config.items()
            if key.startswith("OPENHEART_")
        }
        config.update(options)

        @wraps(app.route)
        def route(rule, **options):
            oh_enabled, oh_config = _get_options(options, config)
            decorator = app._openheart_route(rule, **options)  # noqa: SLF001

            def slug(endpoint):
                def slug_decorator(func):
                    app.openheart.slug_functions[endpoint] = func
                    return func

                return slug_decorator

            @wraps(decorator)
            def wrapper(func):
                endpoint = options.get("endpoint", func.__name__)
                func.slug = slug(endpoint)
                if oh_enabled:
                    oh_rule, oh_endpoint, oh_options = _adapt_rule(oh_config, "GET", rule, endpoint, **options)
                    app.add_url_rule(oh_rule, oh_endpoint, handler, **oh_options)
                    oh_rule, oh_endpoint, oh_options = _adapt_rule(oh_config, "POST", rule, endpoint, **options)
                    app.add_url_rule(oh_rule, oh_endpoint, handler, **oh_options)
                    app.openheart.configs[endpoint] = oh_config
                return decorator(func)

            return wrapper

        app._openheart_route = app.route  # noqa: SLF001 for daisy-chaining the monkey-patched function
        app.route = route
        app.openheart = OpenHeartController()
        app.before_request(before_request)
