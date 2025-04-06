"""The Valkey backend can be used to to store data in a local database file."""

import sqlite3

from flask_openheart.backend.backend import Backend


class SqliteBackend(Backend):
    """The Valkey backend can be used to to store data in a local database file."""

    def _connect(self):
        return sqlite3.connect(self.uri, *self.connect_args, **self.connect_kwargs)

    def incr(self, slug, reaction):
        """Increment the reaction count for a certain reaction on a certain page.

        Args:
            slug: A slug representing the page.
            reaction: The emoji reaction to be incremented.
        """
        cursor = self.connection.cursor()
        table_name = f"{self.namespace}_{slug}"
        query = f'CREATE TABLE IF NOT EXISTS "{table_name}" (reaction TEXT PRIMARY KEY, count INT DEFAULT 1)'
        cursor.execute(query)
        query = f'INSERT INTO "{table_name}" (reaction) VALUES (:reaction) \
            ON CONFLICT (reaction) DO UPDATE SET count=count+1'  # noqa: S608
        cursor.execute(query, {"table_name": table_name, "reaction": reaction})
        self.connection.commit()

    def iter(self, slug):
        """Iterate through all the reactions on a certain page.

        Args:
            slug: A slug representing the page.

        Yields:
            A tuple containing the reaction and the count
        """
        cursor = self.connection.cursor()
        table_name = f"{self.namespace}_{slug}"
        query = f'SELECT reaction, count FROM "{table_name}"'  # noqa: S608
        try:
            result = cursor.execute(query)
        except sqlite3.OperationalError as e:
            if "no such table" in str(e):
                return []
            raise
        return result.fetchall()
