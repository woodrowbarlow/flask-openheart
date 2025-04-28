"""The mapper module provides convenient ways to use OpenHeart reactions programmatically."""

from flask import current_app

from flask_openheart.internal import Storage, get_backend


class OpenHeartController:
    """A Flask extension to add support for OpenHeart protocol."""

    def __init__(self):
        """Initialize a new instance of the OpenHeartExtension."""
        self.configs = {}
        self.slug_functions = {}

    def url_for(self, endpoint, _method=None, **values):
        """Get the OpenHeart URL associated with a given endpoint.

        This function behaves like `flask.url_for`.

        By default this is the GET URL, i.e. the URL used to query reactions. To get the POST URL, i.e. the URL which
        accepts reactions, use the `_method` arg or use `post_url_for` instead.

        :param endpoint: The name of the endpoint which supports OpenHeart.
        :param _method (optional): The HTTP method. Defaults to GET. Supported values: GET, POST.
        :param values: Values to use for the variable parts of the URL rule. Passed to `flask.url_for`.

        :return: The URL for the OpenHeart endpoint associated with the specified endpoint.
        """
        if not self.is_enabled_for(endpoint, **values):
            return None
        if _method is None:
            _method = "GET"
        endpoint = f"openheart.{_method.lower()}.{endpoint}"
        return current_app.url_for(endpoint, **values)

    def post_url_for(self, endpoint, **values):
        """Get the OpenHeart POST URL associated with a given endpoint.

        This is an alias for `url_for` but with the `_method` arg set to "POST".

        :param endpoint: The name of the endpoint which supports OpenHeart.
        :param values: Values to use for the variable parts of the URL rule. Passed to `flask.url_for`.

        :return: The URL for the OpenHeart endpoint associated with the specified endpoint.
        """
        return self.url_for(endpoint, _method="POST", **values)

    def slug_for(self, endpoint, **values):
        """Compute a unique slug for the resource represented by the given endpoint with the given values.

        This function works like `flask.url_for`; provide an endpoint name and the required arguments for that endpoint,
        and get back a result. However, instead of the result being a URL, it is a string that defines how reactions get
        grouped in the database for this endpoint.

        :param endpoint: The endpoint name associated with the slug to generate.
        :param values: Values to use for the variable parts of the URL rule.

        :return: The slug associated with this endpoint (with the given values), as a string.
        """
        if endpoint not in self.configs:
            return None
        if endpoint in self.slug_functions:
            current_app.inject_url_defaults(endpoint, values)
            slug = self.slug_functions[endpoint](**values)
            if slug is not None:
                slug = f"{endpoint}.{slug!s}"
            return slug
        return endpoint

    def reactions_for(self, endpoint, **values):
        """Get all reactions for the given endpoint.

        Similar to `flask.url_for`, you must provide an endpoint name and all of the values needed to build the
        endpoint's URL.

        This function returns a dictionary containing all reactions for that endpoint (with the given values), where the
        reaction is the key and the count is the value.

        :param endpoint: The endpoint name associated with the slug to generate.
        :param values: Values to use for the variable parts of the URL rule.

        :return: The reactions associated with this endpoint (with the given values), as a dict.
        """
        slug = self.slug_for(endpoint, **values)
        if slug is None:
            raise RuntimeError  # TODO better exception
        config = self.configs[endpoint]
        with get_backend(config.database_uri) as backend:
            storage = Storage(backend, slug)
            return storage.reactions

    def react_to(self, reaction, endpoint, **values):
        """Add a reaction for the given endpoint.

        Similar to `flask.url_for`, you must provide an endpoint name and all of the values needed to build the
        endpoint's URL.

        After the reaction is added, the updated set of reactions is returned.

        :param reaction: The desired reaction emoji, as a string, optionally with trailing data.
        :param endpoint: The endpoint name associated with the slug to generate.
        :param values: Values to use for the variable parts of the URL rule.

        :return: The reactions associated with this endpoint (with the given values), as a dict.
        """
        slug = self.slug_for(endpoint, **values)
        if slug is None:
            raise RuntimeError  # TODO better exception
        config = self.configs[endpoint]
        with get_backend(config.database_uri) as backend:
            storage = Storage(backend, slug)
            return storage.react(reaction)

    def config_for(self, endpoint):
        """Get the OpenHeartConfig associated with a given endpoint."""
        return self.configs.get(endpoint, None)

    def is_enabled_for(self, endpoint, **values):
        """Check whether OpenHeart is enabled for a given endpoint.

        :param endpoint: The endpoint name associated with the slug to generate.
        :param values: Values to use for the variable parts of the URL rule.

        :return: True if enabled, False otherwise.
        """
        return self.slug_for(endpoint, **values) is not None


class OpenHeartRequestController:
    """OpenHeartRequest gets attached to each request to expose OpenHeart functionality."""

    def __init__(self, endpoint, **values):
        """Create a new OpenHeartRequest instance.

        :param endpoint: The endpoint name.
        :param values: Values to use for the variable parts of the URL rule.
        """
        self.endpoint = endpoint
        self.values = values

    def _url(self, **args):
        args.update(self.values)
        return current_app.openheart.url_for(self.endpoint, **args)

    @property
    def config(self):
        """The OpenHeart config associated with this request."""
        return current_app.openheart.config_for(self.endpoint)

    @property
    def get_url(self):
        """The OpenHeart reactions GET URL for this request."""
        return self._url()

    @property
    def get_url_external(self):
        """The OpenHeart reactions GET URL for this request, formatted as an external link."""
        return self._url(_external=True)

    @property
    def post_url(self):
        """The OpenHeart reactions POST URL for this request."""
        return self._url(_method="POST")

    @property
    def post_url_external(self):
        """The OpenHeart reactions POST URL for this request, formatted as an external link."""
        return self._url(_method="POST", _external=True)

    @property
    def reactions(self):
        """The OpenHeart reactions for this request."""
        return current_app.reactions_for(self.endpoint, **self.values)

    def react(self, reaction):
        """Add an OpenHeart reaction for this page.

        :param reaction: The desired reaction emoji, as a string, optionally with trailing data.

        :return: The updated reactions, as a dict.
        """
        return current_app.react_to(reaction, self.endpoint, **self.values)
