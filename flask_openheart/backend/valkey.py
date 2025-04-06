"""The valkey backend can be used to connect to Valkey or Redis servers."""

import valkey

from flask_openheart.backend.backend import Backend


class ValkeyBackend(Backend):
    """The Valkey backend can be used to connect to Valkey or Redis servers."""

    def _connect(self):
        return valkey.from_url(self.uri, *self.connect_args, **self.connect_kwargs)

    def incr(self, slug, reaction):
        """Increment the reaction count for a certain reaction on a certain page.

        Args:
            slug: A slug representing the page.
            reaction: The emoji reaction to be incremented.
        """
        self.connection.incr(f"{self.namespace}:{slug}:{reaction}")

    def iter(self, slug):
        """Iterate through all the reactions on a certain page.

        Args:
            slug: A slug representing the page.

        Yields:
            A tuple containing the reaction and the count
        """
        for key in self.connection.scan_iter(f"{self.namespace}:{slug}:*"):
            reaction = key.split(":")[-1]
            count = self.connection.get(f"openheart:{slug}:{reaction}")
            yield reaction, count
