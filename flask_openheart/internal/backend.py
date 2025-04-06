"""A backend supports a storage mechanism such as a database. Multiple backends are available."""

import abc


def get_backend(uri, *args, **kwargs):
    """Get a backend context manager, automatically detecting the type from URI.

    :param uri: The database uri.
    :param args: Additional args passed to the backend connection function.
    :param kwargs: Additional keyword args passed to the backend connection function.

    :exception RuntimeError: Unrecognized URI prefix

    :return: An OpenHeartBackend object (not yet connected).
    """
    if uri.startswith(("file:", "memory:")):
        from flask_openheart.internal.sqlite import SqliteBackend

        return SqliteBackend(uri, *args, **kwargs)
    if uri.startswith(("valkey:", "redis:")):
        from flask_openheart.internal.keystore import ValkeyBackend

        return ValkeyBackend(uri, *args, **kwargs)
    msg = "Unrecognized URI prefix"
    raise RuntimeError(msg)


class BackendError(Exception):
    """Exception raised whenever a backend encounters some kind of database error."""


class Backend(abc.ABC):
    """A simple protocol for allowing emoji-based reactions to URIs."""

    def __init__(self, *args, **kwargs):
        """Create a new OpenHeart controller instance.

        :param args: Positional arguments to be passed to the connection function.
        :param kwargs: Keyword arguments to be passed to the connection function.
        """
        self._args = args
        self._kwargs = kwargs

    def _check_if_connected(self):
        if not self.is_connected():
            raise RuntimeError  # TODO better exception

    @abc.abstractmethod
    def is_connected(self):
        """Check whether the backend is connected.

        :return: True if connected, False otherwise.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def iter(self, slug):
        """Iterate all reactions for a given page.

        :param slug: A slug representing the page.

        :return: A generator yielding: reaction, count.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def incr(self, slug, reaction):
        """Add a reaction for a given page.

        :param slug: A slug representing the page.
        :param reaction: The reaction to add.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def connect(self, *args, **kwargs):
        """Initiate the connection.

        :param args: Positional arguments to pass to the connect function.
        :param kwargs: Keyword arguments to pass to the connect function.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def disconnect(self):
        """Close the connection."""
        raise NotImplementedError

    def __enter__(self):
        """Enter a context manager. This initiates a connection."""
        self.connect(*self._args, **self._kwargs)
        return self

    def __exit__(self, exc_type, exc, traceback):
        """Exit a context manager. This closes the connection."""
        self.disconnect()
