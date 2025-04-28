"""Test cases related to the built-in emoji sanitizer."""

import pytest

from flask_openheart.internal.storage import EMOJI_DATA, InvalidReactionError, sanitize_reaction


class TestEmojiSanitizer:
    """Test cases for the sanitize_reaction function."""

    def test_invalid_data(self):
        """Test that various invalid reactions all raise the appropriate error."""
        for reaction in ["", "foo", " ❤️", 0, None]:
            with pytest.raises(InvalidReactionError):
                sanitize_reaction(reaction)

    def test_trailing_data(self):
        """Test that an emoji with trailing data gets separated correctly."""
        e, remainder = sanitize_reaction("❤️=")
        assert e == "❤️"
        assert remainder == "="

    def test_all_emojis(self):
        """Test that all emojis in the test data are accepted."""
        for emoji, details in EMOJI_DATA.items():
            e, remainder = sanitize_reaction(emoji)
            assert e == emoji, f"failed to validate: {emoji} ({details['description']})"
            assert not remainder, f"returned remainder: {emoji} ({details['description']})"
