"""Utility functions for examples tests."""

import http
import json


def _test_enabled_reactions(client, path, post_path=None, reaction=None):
    if post_path is None:
        post_path = path
    if reaction is None:
        reaction = "❤️"
    response = client.get(path)
    assert response.status_code == http.HTTPStatus.OK
    orig_count = json.loads(response.data).get(reaction, 0)
    response = client.post(post_path, data=reaction.encode())
    assert response.status_code == http.HTTPStatus.OK
    final_count = json.loads(response.data).get(reaction, 0)
    assert final_count > orig_count


def _test_disabled_reactions(client, path, post_path=None, reaction=None):
    if post_path is None:
        post_path = path
    if reaction is None:
        reaction = "❤️"
    response = client.get(path)
    assert response.status_code != http.HTTPStatus.OK
    response = client.post(post_path, data=reaction.encode())
    assert response.status_code != http.HTTPStatus.OK
