"""Test cases for the 'basic' example."""

import http

from bs4 import BeautifulSoup

from examples.basic.app import app
from tests.examples.util import _test_disabled_reactions, _test_enabled_reactions


def _test_page_title(soup, title):
    title_element = soup.find("h1")
    assert title_element.text == title


def _test_enabled_footer(soup, get_url, set_url=None):
    if set_url is None:
        set_url = get_url
    element = soup.find_all("hr")[-1].find_next_sibling("p")
    expected_text = "This page supports emoji-based reactions via the OpenHeart protocol"
    actual_text = " ".join(element.stripped_strings)
    assert actual_text.startswith(expected_text)
    element = element.find_next_sibling("pre")
    assert get_url in element.get_text()
    element = element.find_next_sibling("pre")
    assert set_url in element.get_text()


def _test_disabled_footer(soup):
    footer_element = soup.find_all("hr")[-1].find_next_sibling("p")
    expected_text = "OpenHeart reactions are not supported on this page"
    actual_text = " ".join(footer_element.stripped_strings)
    assert actual_text.startswith(expected_text)


class TestBasicExample:
    """Test cases for the 'basic' example."""

    def test_index_body(self):
        """A test to be sure the index contains the expected body content."""
        client = app.test_client()
        response = client.get("/")
        assert response.status_code == http.HTTPStatus.OK
        soup = BeautifulSoup(response.data, "html.parser")
        _test_page_title(soup, "index")
        _test_enabled_footer(soup, "http://localhost/openheart/")

    def test_index_reactions(self):
        """A test to be sure the index page accepts reactions."""
        client = app.test_client()
        _test_enabled_reactions(client, "/openheart/")

    def test_foo_body(self):
        """A test to be sure the foo page contains the expected body content."""
        client = app.test_client()
        response = client.get("/foo/")
        assert response.status_code == http.HTTPStatus.OK
        soup = BeautifulSoup(response.data, "html.parser")
        _test_page_title(soup, "foo")
        _test_enabled_footer(soup, "http://localhost/openheart/foo/")

    def test_foo_reactions(self):
        """A test to be sure the foo page accepts reactions."""
        client = app.test_client()
        _test_enabled_reactions(client, "/openheart/foo/")

    def test_bar_body(self):
        """A test to be sure the bar page contains the expected body content."""
        client = app.test_client()
        response = client.get("/bar/")
        assert response.status_code == http.HTTPStatus.OK
        soup = BeautifulSoup(response.data, "html.parser")
        _test_page_title(soup, "bar")
        _test_disabled_footer(soup)

    def test_bar_reactions(self):
        """A test to be sure the bar page does not accept reactions."""
        client = app.test_client()
        _test_disabled_reactions(client, "/openheart/bar/")
