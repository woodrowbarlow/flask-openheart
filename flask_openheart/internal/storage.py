"""The storage is an interface between the extension and the backend."""

from emoji import EMOJI_DATA

from flask_openheart.internal.backend import get_backend


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

    :param data: Input data from the user.

    :exception InvalidReactionError: If the input data does not match a valid emoji.

    :return: The matching emoji.
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
    return match, data[len(match) :]


class Storage:
    """The storage is an interface between the extension and the backend."""

    def __init__(self, slug, config):
        """Create a new instance of OpenHeartStorage.

        :param config: An instance of OpenHeartConfig.
        :param slug: A slug representing the page.
        """
        self.slug = slug
        self.config = config
        self.backend = None

    def _check_if_connected(self):
        if self.backend is None:
            raise RuntimeError  # TODO better exception

    @property
    def reactions(self):
        """Get all reactions for a given page, as a dict.

        :return: A dict in which the reactions are the keys and the counts are the values.
        """
        self._check_if_connected()
        return dict(self.backend.iter(self.slug))

    def react(self, reaction):
        """Add a reaction for a given page.

        :param reaction: The reaction to add.

        :return: The updated reactions, as a dict.
        """
        self._check_if_connected()
        reaction = sanitize_reaction(reaction)[0]
        self.backend.incr(self.slug, reaction)
        return self.reactions

    def __enter__(self):
        """Enter a conectext manager. This initiates a connection."""
        self.backend = get_backend(self.config.database_uri)
        self.backend.__enter__()
        return self

    def __exit__(self, exc_type, exc, traceback):
        """Exit a conectext manager. This closes the connection."""
        if self.backend is None:
            return
        self.backend.__exit__(exc_type, exc, traceback)
        self.backend = None
