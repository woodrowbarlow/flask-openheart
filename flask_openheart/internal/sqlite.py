"""The Sqlite backend can be used to to store data in a local database file."""

import sqlite3

from flask_openheart.internal import Backend, BackendError


class SqliteBackend(Backend):
    """The Sqlite backend can be used to to store data in a local database file."""

    def __init__(self, *args, **kwargs):
        """Create a new Sqlite backend instance.

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
            self.connection = sqlite3.connect(uri, *args, **kwargs)
        except sqlite3.DatabaseError as e:
            self.connection = None
            msg = "A database error occurred while connecting."
            raise BackendError(msg) from e

    def disconnect(self):
        """Close the connection."""
        self.connection.close()
        self.connection = None

    def is_connected(self):
        """Check whether the backend is connected.

        Returns:
            True if connected, False otherwise.
        """
        return self.connection is not None

    def _create(self, cursor):
        query = """
                CREATE TABLE IF NOT EXISTS openheart ( \
                    slug TEXT, \
                    reaction TEXT, \
                    count INT DEFAULT 1, \
                    PRIMARY KEY (slug, reaction) \
                )
            """
        try:
            cursor.execute(query)
        except sqlite3.DatabaseError as e:
            msg = "A database error occurred while setting up the table."
            raise BackendError(msg) from e

    def incr(self, slug, reaction):
        """Increment the reaction count for a certain reaction on a certain page.

        :param slug: A slug representing the page.
        :param reaction: The emoji reaction to be incremented.
        """
        self._check_if_connected()
        cursor = self.connection.cursor()
        self._create(cursor)
        query = """
                INSERT INTO openheart (slug, reaction) VALUES (:slug, :reaction)
                    ON CONFLICT (slug, reaction) DO UPDATE SET count=count+1
            """
        try:
            cursor.execute(query, {"slug": slug, "reaction": reaction})
            self.connection.commit()
        except sqlite3.DatabaseError as e:
            msg = f"A database error occurred while processing a reaction for '{slug}'."
            raise BackendError(msg) from e

    def iter(self, slug):
        """Iterate through all the reactions on a certain page.

        :param slug: A slug representing the page.

        :return: A generator yielding: reaction, count.
        """
        self._check_if_connected()
        cursor = self.connection.cursor()
        self._create(cursor)
        query = """
                SELECT reaction, count FROM openheart WHERE slug=:slug
            """
        try:
            result = cursor.execute(query, {"slug": slug})
        except sqlite3.DatabaseError as e:
            msg = f"A database error occurred while querying reactions for '{slug}'."
            raise BackendError(msg) from e
        row = result.fetchone()
        while row:
            yield row
            row = result.fetchone()
