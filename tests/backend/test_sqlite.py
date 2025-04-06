"""Test cases for the SQLiteBackend object."""

from collections.abc import Sequence

import pytest

from flask_openheart.internal.sqlite import SqliteBackend


def _is_sequence(obj):
    return isinstance(obj, Sequence) and not isinstance(obj, str | bytes | bytearray)


def _table_exists(conn, table_name):
    cursor = conn.cursor()
    query = 'SELECT name FROM sqlite_master WHERE type="table" AND name=:table_name'
    result = cursor.execute(query, {"table_name": table_name})
    return result.fetchone() is not None


@pytest.fixture
def backend():
    """Pytest fixture to easily generate an in-memory SQLite backend for testing.

    Yields:
        SqliteBackend: The in-memory SQLite backend object.
    """
    uri = ":memory:"
    namespace = "test"
    with SqliteBackend(uri, namespace) as backend:
        yield backend


class TestSqliteBackend:
    """Test cases for the SQLiteBackend object."""

    def test_constructor(self, backend):
        """Test that basic properties were set up correctly.

        Args:
            backend: The SQLite backend (supplied by fixture).
        """
        assert backend is not None
        assert backend.connection is not None
        assert backend.namespace == "test"
        table_name = backend.table_name("foo")
        assert "foo" in table_name
        assert backend.namespace in table_name

    def test_iter_incr(self, backend):
        """Test that iterating on a slug which does not exist should return an empty collection.

        Args:
            backend: The SQLite backend (supplied by fixture).
        """
        slug = "foo"
        other_slug = "bar"
        reaction = "❤️"
        other_reaction = "🥨"
        table_name = backend.table_name(slug)
        assert not _table_exists(backend.connection, table_name)
        results = backend.iter(slug)
        assert _is_sequence(results)
        assert len(results) == 0
        assert not _table_exists(backend.connection, table_name)
        backend.incr(slug, reaction)
        assert _table_exists(backend.connection, table_name)
        results = backend.iter(slug)
        assert _is_sequence(results)
        assert len(results) == 1
        actual_reaction, count = results[0]
        assert actual_reaction == reaction
        assert count == 1
        backend.incr(slug, reaction)
        results = backend.iter(slug)
        assert len(results) == 1
        actual_reaction, count = results[0]
        assert actual_reaction == reaction
        assert count == 2
        backend.incr(slug, other_reaction)
        results = backend.iter(slug)
        assert len(results) == 2
        actual_reaction, count = results[0]
        assert actual_reaction == reaction
        assert count == 2
        actual_reaction, count = results[1]
        assert actual_reaction == other_reaction
        assert count == 1
        backend.incr(other_slug, reaction)
        assert _table_exists(backend.connection, backend.table_name(other_slug))
        assert _table_exists(backend.connection, table_name)
        results = backend.iter(other_slug)
        assert len(results) == 1
        results = backend.iter(slug)
        assert len(results) == 2
