Configuration
=============

Options
-------

The following Flask Configuration values are honored by Flask-OpenHeart. If the corresponding argument is also provided
to the ``OpenHeart.init_app()`` method, then the init argument will take priority. Per-endpoint configuration takes
priority over all other configuration.

.. list-table:: Configuration Options
    :header-rows: 1

    * - Option
      - Description

    * - OPENHEART_DATABASE_URI

        init arg: ``database_uri``

      - The databaase URI, for storing reactions.

        Default: ``file:openheart.db``

    * - OPENHEART_URL_PREFIX

        init arg: ``url_prefix``

      - The URL prefix for the OpenHeart endpoints.

        Default: ``/opeheart``

    * - OPENHEART_URL_POST_PREFIX

        init arg: ``post_url_prefix``

      - The URL prefix for the OpenHeart POST endpoint, if different.

        Default: The value of ``OPENHEART_URL_PREFIX``

Global Configuration
--------------------

Application configuration can be set by environment variables, by prefixing "FLASK\_" to the config key. For example, to
run an application with a custom URL prefix:

.. code-block:: shell

    FLASK_APP=app:app FLASK_OPENHEART_URL_PREFIX=/reactions flask run

It can, of course, also be set in the application code before calling ``OpenHeart.init_app()``:

.. code-block:: python

    from flask import Flask
    from flask_openheart import OpenHeart

    app = Flask(__name__)
    app.config["OPENHEART_URL_PREFIX"] = "/reactions"
    openheart = OpenHeart()
    openheart.init_app(app)

Or as arguments to ``OpenHeart.init_app()`` (which take priority over the app config and environment variables):

.. code-block:: python

    from flask import Flask
    from flask_openheart import OpenHeart

    app = Flask(__name__)
    openheart = OpenHeart()
    openheart.init_app(app, url_prefix="/reactions")

Per-Endpoint Configuration
--------------------------

It is also possible to set any of these configuration values on a per-endpoint basis. Instead of passing `True` for the
`openheart` argument, you can pass a dictionary of configuration options. This dictionary uses the same key names as the
``OpenHeart.init_app()`` method. Configuration set in this way takes priority over all other configuration.

To set configuration for a specific route:

.. code-block:: python

    @app.route("/foo/", openheart={ "url_prefix"="/reactions" })
    def foo():
        return "bar"

Database Configuration
----------------------

Flask-OpenHeart stores all reactions in a database. Multiple different types of databases are supported. By default,
reactions are stored in a local flat-file database powered by SQLite.

SQLite (local file)
^^^^^^^^^^^^^^^^^^^

The SQLite backend can create a local single-file database and store all reactions there. By default, this file is named
"openheart.db" and gets stored in the current working directory (where you ran ``flask run``).

To use the SQLite backend and specify the location of the database, set the ``OPENHEART_DATABASE_URI`` config value to a
file URI, starting with "file:".

For example:

.. code-block:: python

    app.config["OPENHEART_DATABASE_URI"] = "file:/tmp/reactions.db"

    openheart = OpenHeart()
    openheart.init_app(app)

Or:

.. code-block:: python

    openheart = OpenHeart()
    openheart.init_app(app, database_uri="file:/tmp/reactions.db")

For details on how to structure the URI, please see the
`SQLite documentation for URIs <https://www.sqlite.org/uri.html>`_

Valkey/Redis
^^^^^^^^^^^^

The Valkey backend can connect to a Valkey (or Redis) server and store all reactions there.

The Valkey dependencies are not installed by default. To install the Valkey dependencies, run:

.. code-block:: shell

    pip install flask-openheart[valkey]

To use the Valkey backend, set the ``OPENHEART_DATABASE_URI`` config value to a valid Valkey or Redis database URI,
starting with either "valkey:" or "redis:".

For example:

.. code-block:: python

    app.config["OPENHEART_DATABASE_URI"] = "valkey://127.0.0.1:6369"

    openheart = OpenHeart()
    openheart.init_app(app)

Or:

.. code-block:: python

    openheart = OpenHeart()
    openheart.init_app(app, database_uri="valkey://127.0.0.1:6369")

For details on how to structure the URI, please see
`valkey.Valkey.from_url() <https://valkey-py.readthedocs.io/en/latest/connections.html#valkey.Valkey.from_url>`_
