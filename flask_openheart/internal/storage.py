"""The storage is an interface between the extension and the backend."""

import importlib
import json


def _get_path(name):
    return importlib.resources.files("flask_openheart.internal").joinpath(name)


with _get_path("emoji.json").open("rb") as f:
    EMOJI_DATA = json.load(f)


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
    if not data:
        msg = "No emoji data supplied."
        raise InvalidReactionError(msg)
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

    def __init__(self, backend, slug, allowed=None, blocked=None, defaults=None):
        """Create a new instance of OpenHeartStorage.

        :param slug: A slug representing the page.
        """
        self.backend = backend
        self.slug = slug
        self.allowed = allowed
        self.blocked = blocked
        self.defaults = defaults

    @property
    def reactions(self):
        """Get all reactions for a given page, as a dict.

        :return: A dict in which the reactions are the keys and the counts are the values.
        """
        result = {}
        for reaction, count in self.backend.iter(self.slug):
            if self.allowed is not None and reaction not in self.allowed:
                continue
            if self.blocked is not None and reaction in self.blocked:
                continue
            result[reaction] = count
        if self.defaults is not None:
            for reaction, count in self.defaults.items():
                if reaction in result:
                    result[reaction] += count
                else:
                    result[reaction] = count
        return result

    def react(self, reaction):
        """Add a reaction for a given page.

        :param reaction: The reaction to add.

        :return: The updated reactions, as a dict.
        """
        reaction = sanitize_reaction(reaction)[0]
        if self.allowed is not None and reaction not in self.allowed:
            msg = "This emoji is not allowed."
            raise InvalidReactionError(msg)
        if self.blocked is not None and reaction in self.blocked:
            msg = "This emoji is blocked."
            raise InvalidReactionError(msg)
        self.backend.incr(self.slug, reaction)
        return self.reactions
