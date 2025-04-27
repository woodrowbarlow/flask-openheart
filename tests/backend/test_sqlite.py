"""Test cases for the SQLiteBackend object."""

import pytest

from flask_openheart.internal.sqlite import SqliteBackend


def _table_exists(conn):
    cursor = conn.cursor()
    query = 'SELECT name FROM sqlite_master WHERE type="table" AND name="openheart"'
    result = cursor.execute(query)
    return result.fetchone() is not None


def _get_table(conn):
    cursor = conn.cursor()
    query = "SELECT * FROM pragma_table_info('openheart')"
    result = cursor.execute(query)
    keys = [row[1] for row in result.fetchall()]
    if len(keys) == 0:
        return []
    query = "SELECT * FROM openheart"
    result = cursor.execute(query)
    return [dict(zip(keys, row, strict=False)) for row in result.fetchall()]


@pytest.fixture
def backend():
    """Pytest fixture to easily generate an in-memory SQLite backend for testing.

    Yields:
        SqliteBackend: The in-memory SQLite backend object.
    """
    uri = ":memory:"
    with SqliteBackend(uri) as backend:
        yield backend


class TestSqliteBackend:
    """Test cases for the SQLiteBackend object."""

    def test_iter_no_create_table(self, backend):
        """Test that iterating on an empty database does not create a table.

        :param backend: The SQLite backend (supplied by fixture).
        """
        slug = "foo"
        assert not _table_exists(backend.connection)
        results = list(backend.iter(slug))
        assert len(results) == 0
        assert not _table_exists(backend.connection)

    def test_incr_create_table(self, backend):
        """Test that incrementing a reaction on an empty database creates a table.

        :param backend: The SQLite backend (supplied by fixture).
        """
        slug = "foo"
        reaction = "❤️"
        assert not _table_exists(backend.connection)
        backend.incr(slug, reaction)
        assert _table_exists(backend.connection)

    def test_incr_performs_insert(self, backend):
        """Test that incrementing a reaction on an empty database causes it to be inserted into the database.

        :param backend: The SQLite backend (supplied by fixture).
        """
        slug = "foo"
        reaction = "❤️"
        backend.incr(slug, reaction)
        table = _get_table(backend.connection)
        assert len(table) == 1
        row = table[0]
        assert slug in row["slug"]
        assert row["reaction"] == reaction
        assert row["count"] == 1

    def test_incr_iter(self, backend):
        """Test that incrementing a reaction causes it to show up when iterating.

        :param backend: The SQLite backend (supplied by fixture).
        """
        slug = "foo"
        reaction = "❤️"
        backend.incr(slug, reaction)
        iterator = backend.iter(slug)
        actual_reaction, count = next(iterator)
        assert actual_reaction == reaction
        assert count == 1
        with pytest.raises(StopIteration):
            next(iterator)

    def test_incr_count(self, backend):
        """Test that the "count" field gets incremented each time we increment a reaction.

        :param backend: The SQLite backend (supplied by fixture).
        """
        slug = "foo"
        reaction = "❤️"
        backend.incr(slug, reaction)
        actual_reaction, count = next(backend.iter(slug))
        assert actual_reaction == reaction
        assert count == 1
        backend.incr(slug, reaction)
        actual_reaction, count = next(backend.iter(slug))
        assert actual_reaction == reaction
        assert count == 2
        backend.incr(slug, reaction)
        actual_reaction, count = next(backend.iter(slug))
        assert actual_reaction == reaction
        assert count == 3

    def test_reactions_distinct(self, backend):
        """Test that incrementing one reaction does not affect the count for another reaction.

        :param backend: The SQLite backend (supplied by fixture).
        """
        slug = "foo"
        reaction = "❤️"
        other_reaction = "🥨"
        backend.incr(slug, reaction)
        backend.incr(slug, reaction)
        backend.incr(slug, other_reaction)
        results = dict(backend.iter(slug))
        assert len(results) == 2
        assert results[reaction] == 2
        assert results[other_reaction] == 1

    def test_slugs_distinct(self, backend):
        """Test that incrementing reactions on one slug does not affect the counts for another slug.

        :param backend: The SQLite backend (supplied by fixture).
        """
        slug = "foo"
        other_slug = "bar"
        reaction = "❤️"
        other_reaction = "🥨"
        backend.incr(slug, reaction)
        backend.incr(slug, reaction)
        backend.incr(other_slug, reaction)
        backend.incr(other_slug, other_reaction)
        results = dict(backend.iter(slug))
        assert len(results) == 1
        assert results[reaction] == 2
        results = dict(backend.iter(other_slug))
        assert len(results) == 2
        assert results[reaction] == 1
