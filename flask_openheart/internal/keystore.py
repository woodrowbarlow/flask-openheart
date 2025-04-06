"""The valkey backend can be used to connect to Valkey or Redis servers."""

import valkey

from flask_openheart.internal import Backend, BackendError


class ValkeyBackend(Backend):
    """The Valkey backend can be used to connect to Valkey or Redis servers."""

    def __init__(self, *args, **kwargs):
        """Create a new Valkey backend instance.

        :param args: Positional arguments to be passed to the connection function.
        :param kwargs: Keyword arguments to be passed to the connection function.
        """
        super().__init__(*args, **kwargs)
        self.connection = None

    def connect(self, uri, *args, **kwargs):
        """Initiate the connection.

        :param uri: The database URI.
        :param args: Extra positional arguments to pass to the connect function.
        :param kwargs: Extra keyword arguments to pass to the connect function.
        """
        if self.connection is not None:
            self.disconnect()

        try:
            self.connection = valkey.from_url(uri, *args, **kwargs)
        except valkey.exceptions.ConnectionError as e:
            self.connection = None
            msg = "A database error occurred while connecting."
            raise BackendError(msg) from e

    def disconnect(self):
        """Close the connection."""
        self.connection.close()
        self.connection = None

    def is_connected(self):
        """Check whether the backend is connected.

        :return: True if connected, False otherwise.
        """
        return self.connection is not None

    def incr(self, slug, reaction):
        """Increment the reaction count for a certain reaction on a certain page.

        :param slug: A slug representing the page.
        :param reaction: The emoji reaction to be incremented.
        """
        self._check_if_connected()
        try:
            self.connection.incr(f"openheart:{slug}:{reaction}")
        except valkey.exceptions.ValkeyError as e:
            msg = f"A database error occurred while processing a reaction for '{slug}'."
            raise BackendError(msg) from e

    def iter(self, slug):
        """Iterate through all the reactions on a certain page.

        :param slug: A slug representing the page.

        :return: A generator yielding: reaction, count.
        """
        self._check_if_connected()
        try:
            generator = self.connection.scan_iter(f"openheart:{slug}:*")
        except valkey.exceptions.ValkeyError as e:
            msg = f"A database error occurred while querying reactions for '{slug}'."
            raise BackendError(msg) from e

        for key in generator:
            reaction = key.split(":")[-1]
            try:
                count = self.connection.get(f"openheart:{slug}:{reaction}")
            except valkey.exceptions.ValkeyError as e:
                msg = f"A database error occurred while querying reactions for '{slug}'."
                raise BackendError(msg) from e
            yield reaction, count
