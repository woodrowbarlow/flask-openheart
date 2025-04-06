"""Abstract class definitions for all backends."""

import abc


class Backend(abc.ABC):
    """A backend object handles all calls to the database."""

    def __init__(self, uri, namespace, *args, **kwargs):
        """Create a new backend instance.

        Args:
            uri: The database URI.
            namespace: The database namespace.
            args: Extra arguments to pass to the db connection function.
            kwargs: Extra keyword arguments to pass to the db connection function.
        """
        self.uri = uri
        self.namespace = namespace
        self.connect_args = args
        self.connect_kwargs = kwargs
        self.connection = None

    @abc.abstractmethod
    def incr(self, slug, reaction):
        """Increment the reaction count for a certain reaction on a certain page.

        Args:
            slug: A slug representing the page.
            reaction: The emoji reaction to be incremented.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def iter(self, slug):
        """Iterate through all the reactions on a certain page.

        Args:
            slug: A slug representing the page.

        Yields:
            A tuple containing the reaction and the count
        """
        raise NotImplementedError

    @abc.abstractmethod
    def _connect(self):
        """Initiate the connection."""
        raise NotImplementedError

    def connect(self):
        """Initiate the connection."""
        self.close()
        self.connection = self._connect()

    def close(self):
        """Close the connection."""
        if self.connection is None:
            return
        self.connection.close()
        self.connection = None

    def __enter__(self):
        """Open a conectext manager. This is equivalent to calling "connect"."""
        self.connect()
        return self

    def __exit__(self, exc_type, exc, traceback):
        """Open a conectext manager. This is equivalent to calling "close"."""
        self.close()
