"""A simple protocol for allowing emoji-based reactions to URIs."""

from emoji import EMOJI_DATA

from flask_openheart.backend import get_backend


class InvalidReactionError(Exception):
    """An invalid reaction error occurs when user input does not represent any approved emoji."""

    def __init__(self, message):
        """Create a new instance of InvalidReactionError.

        Args:
            message: The user-facing error message.
        """
        self.message = message

    def __str__(self):
        """Returns the user-facing error message.

        Returns:
            The user-facing error message.
        """
        return self.message


def sanitize_reaction(data):
    """Check that the data matches OpenHeart spec and strip extraneous data.

    Args:
        data: Input data from the user.

    Raises:
        InvalidReactionError: If the input data does not match a valid emoji.

    Returns:
        The matching emoji.
    """
    match = None
    emojis = EMOJI_DATA.keys()
    for emoji in emojis:
        if match is not None and len(match) >= len(emoji):
            continue
        if data.startswith(emoji):
            match = emoji
    if match is None:
        msg = "This is not a recognized emoji."
        raise InvalidReactionError(msg)
    return match


class OpenHeart:
    """A simple protocol for allowing emoji-based reactions to URIs."""

    def __init__(self, database_uri, database_prefix):
        """Create a new OpenHeart controller instance.

        Args:
            database_uri: The database URI, for the storage backend.
            database_prefix: The database namespace, used to prefix keys or table names.
        """
        self._database_uri = database_uri
        self._database_prefix = database_prefix

    def _reactions(self, backend, slug):
        return dict(backend.iter(slug))

    def _react(self, backend, slug, reaction):
        backend.incr(slug, reaction)

    def reactions(self, slug):
        """Get all reactions for a given page.

        Args:
            slug: A slug representing the page.
        """
        with get_backend(self._database_uri, self._database_prefix) as backend:
            return self._reactions(backend, slug)

    def react(self, slug, reaction):
        """Add a reaction for a given page.

        Args:
            slug: A slug representing the page.
            reaction: The reaction to add.
        """
        reaction = sanitize_reaction(reaction)
        with get_backend(self._database_uri, self._database_prefix) as backend:
            self._react(backend, slug, reaction)
            return self._reactions(backend, slug)
