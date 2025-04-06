"""Configuration for OpenHeart-enabled endpoints."""

DEFAULT_DATABASE_URI = "file:openheart.db"
DEFAULT_URL_PREFIX = "/openheart"


class OpenHeartConfig(dict):
    """An object to represent Flask-OpenHeart configuration options."""

    @property
    def database_uri(self):
        """The database URI."""
        return self.get("database_uri", DEFAULT_DATABASE_URI)

    @property
    def url_prefix(self):
        """The URL prefix for OpenHeart API requests."""
        return self.get("url_prefix", DEFAULT_URL_PREFIX)

    @property
    def post_url_prefix(self):
        """The URL prefix for OpenHeart API SET requests. Defaults to `url_prefix`."""
        return self.get("post_url_prefix", self.url_prefix)
