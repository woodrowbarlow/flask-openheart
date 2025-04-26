"""Test cases for the 'slugging' example."""

import http
import json

from examples.slugging.app import app
from examples.slugging.data import pages
from tests.examples.util import _test_disabled_reactions, _test_enabled_reactions


def _get_count(client, path, reaction):
    response = client.get(path)
    assert response.status_code == http.HTTPStatus.OK
    return json.loads(response.data).get(reaction, 0)


def _react_and_count(client, path, reaction):
    response = client.post(path, data=reaction.encode())
    assert response.status_code == http.HTTPStatus.OK
    return json.loads(response.data).get(reaction, 0)


class TestSluggingExample:
    """Test cases for the 'slugging' example."""

    def test_index(self):
        """Test that the index page exists."""
        client = app.test_client()
        response = client.get("/")
        assert response.status_code == http.HTTPStatus.OK

    def test_valid_pages(self):
        """Test that each page has a functional OpenHeart endpoint."""
        client = app.test_client()
        for i in range(len(pages)):
            _test_enabled_reactions(client, f"/openheart/page/{i}/")

    def test_invalid_pages(self):
        """Test that non-existent pages do not have a functioning OpenHeart endpoint."""
        client = app.test_client()
        for i in [-1, "foo", len(pages)]:
            _test_disabled_reactions(client, f"/openheart/page/{i}/")

    def test_reactions_distinct(self):
        """Test that reacting to one page does not impact the reactions of another page."""
        client = app.test_client()
        reaction = "❤️"
        paths = [f"/openheart/page/{i}/" for i in range(2)]
        original_counts = [_get_count(client, paths[i], reaction) for i in range(2)]
        counts = [0, 0]
        counts[0] = _react_and_count(client, paths[0], reaction)
        counts[1] = _get_count(client, paths[1], reaction)
        assert counts[1] < counts[0]
        assert counts[0] != original_counts[0]
        assert counts[1] == original_counts[1]
