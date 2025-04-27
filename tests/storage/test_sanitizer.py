"""Test cases related to the built-in emoji sanitizer."""

import urllib

import pytest

from flask_openheart.internal.storage import InvalidReactionError, sanitize_reaction


@pytest.fixture(scope="session")
def emoji_test_file(tmp_path_factory):
    """Test fixture to download the Unicode 16.0 emoji test data."""
    url = "https://unicode.org/Public/emoji/16.0/emoji-test.txt"
    path = tmp_path_factory.mktemp("data") / "emoji-test.txt"
    with urllib.request.urlopen(url) as src, path.open("wb") as dest:  # noqa: S310
        dest.write(src.read())
    return path


def iter_emoji_lines(file):
    """Helper function that iterates through the test data file and yields each line containing an emoji."""
    group = None
    subgroup = None
    for line in file:
        if not line.strip():
            continue
        if not line.startswith("#"):
            yield group, subgroup, line
        elif line.startswith("# group:"):
            group = line.split(":", maxsplit=1)[1]
            group = group.strip()
        elif line.startswith("# subgroup:"):
            subgroup = line.split(":", maxsplit=1)[1]
            subgroup = subgroup.strip()


def parse_emoji_line(line):
    """Helper function that processes data containing an emoji, breaking it into sub-parts."""
    parts = line.strip().split(";", maxsplit=1)
    codepoints_str = parts[0].strip()
    line = parts[1].strip()
    parts = line.split("#", maxsplit=1)
    status = parts[0].strip()
    description = parts[1].strip()
    emoji = "".join(chr(int(code, 16)) for code in codepoints_str.split())
    return emoji, status, description


@pytest.fixture(scope="session")
def emoji_details(emoji_test_file):
    """Test fixture to get all emojis from the test file."""
    details = []
    with emoji_test_file.open() as f:
        for group, subgroup, line in iter_emoji_lines(f):
            emoji, status, description = parse_emoji_line(line)
            details.append(
                {
                    "group": group,
                    "subgroup": subgroup,
                    "emoji": emoji,
                    "status": status,
                    "description": description,
                }
            )
    return details


class TestEmojiSanitizer:
    """Test cases for the sanitize_reaction function."""

    def test_sanitizer_empty(self):
        """Test that en empty string causes an error."""
        with pytest.raises(InvalidReactionError):
            sanitize_reaction("")

    def test_all_emojis(self, emoji_details):
        """Test that all emojis in the test data are accepted."""
        for details in emoji_details:
            e, remainder = sanitize_reaction(details["emoji"])
            assert e == details["emoji"], f"failed to validate: {details['description']}"
            assert not remainder, f"returned remainder: {details['description']}"
