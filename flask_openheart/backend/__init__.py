"""A backend supports a storage mechanism such as a database. Multiple backends are available."""


def get_backend(uri, namespace, *args, **kwargs):
    """Get a backend context manager, automatically detecting the type from URI.

    Args:
        uri: The database uri.
        namespace: The database namespace.
        args: Additional args passed to the backend connection function.
        kwargs: Additional keyword args passed to the backend connection function.

    Raises:
        RuntimeError: Unrecognized URI prefix

    Returns:
        BackendContext: The context manager for the backend.
    """
    if uri.startswith("file:"):
        from flask_openheart.backend.sqlite import SqliteBackend

        return SqliteBackend(uri, namespace, *args, **kwargs)
    if uri.startswith(("valkey:", "redis:")):
        from flask_openheart.backend.valkey import ValkeyBackend

        return ValkeyBackend(uri, namespace, *args, **kwargs)
    msg = "Unrecognized URI prefix"
    raise RuntimeError(msg)
