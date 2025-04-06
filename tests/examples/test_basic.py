"""Test cases for the 'basic' example."""

from examples.basic.app import app


def test_request_example():
    """A test to be sure the index contains the expected body content."""
    client = app.test_client()
    response = client.get("/")
    assert b"hello world" in response.data
