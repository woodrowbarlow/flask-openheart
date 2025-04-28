"""Test cases related to the storage layer."""

import pytest

from flask_openheart.internal import Storage
from flask_openheart.internal.sqlite import SqliteBackend


@pytest.fixture
def test_data():
    """Pytest fixture containing some initial data to populate into the backend."""
    return {
        "foo": {
            "❤️": 3,
            "🥨": 1,
        },
    }


@pytest.fixture
def backend(test_data):
    """Pytest fixture to easily generate an in-memory SQLite backend for testing.

    Yields:
        SqliteBackend: The in-memory SQLite backend object.
    """
    uri = ":memory:"
    with SqliteBackend(uri) as backend:
        for slug, defaults in test_data.items():
            for reaction, count in defaults.items():
                for _ in range(count):
                    backend.incr(slug, reaction)
        yield backend


class TestStorageLayer:
    """Test cases related to the storage layer."""

    def test_no_options(self, backend):
        """Test that a storage layer with no options behaves reasonably."""
        storage = Storage(backend, "foo")
        assert len(storage.reactions) == 2
        assert storage.reactions["❤️"] == 3

    def test_allowed(self, backend):
        """Test that the allow-list can be used to filter reactions."""
        storage = Storage(backend, "foo", allowed=["❤️"])
        assert len(storage.reactions) == 1
        assert "🥨" not in storage.reactions
        assert storage.reactions["❤️"] == 3

    def test_blocked(self, backend):
        """Test that the block-list can be used to filter reactions."""
        storage = Storage(backend, "foo", blocked=["🥨"])
        assert len(storage.reactions) == 1
        assert "🥨" not in storage.reactions
        assert storage.reactions["❤️"] == 3

    def test_block_allowed(self, backend):
        """Test that the allow-list and block-list interact as expected."""
        storage = Storage(backend, "foo", allowed=["❤️", "🥨"], blocked=["🥨"])
        assert len(storage.reactions) == 1
        assert "🥨" not in storage.reactions
        assert storage.reactions["❤️"] == 3

    def test_defaults(self, backend):
        """Test that the defaults-list can be used to augment reactions."""
        storage = Storage(backend, "foo", defaults={"🥨": 5, "😺": 2})
        assert len(storage.reactions) == 3
        assert storage.reactions["🥨"] == 6
        assert storage.reactions["😺"] == 2

    def test_allowed_default(self, backend):
        """Test that the defaults-list bypasses the allow-list."""
        storage = Storage(backend, "foo", allowed=["❤️"], defaults={"❤️": 5, "🥨": 2})
        assert len(storage.reactions) == 2
        assert storage.reactions["🥨"] == 2
        assert storage.reactions["❤️"] == 8

    def test_blocked_default(self, backend):
        """Test that the defaults-list bypasses the block-list."""
        storage = Storage(backend, "foo", blocked=["🥨"], defaults={"🥨": 5, "😺": 2})
        assert len(storage.reactions) == 3
        assert storage.reactions["🥨"] == 5
