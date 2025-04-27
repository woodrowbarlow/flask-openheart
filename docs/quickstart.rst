Quickstart
===========

Install Flask-OpenHeart
-----------------------

.. code-block:: shell

    pip install flask-openheart

Enable OpenHeart Support
------------------------

After initializing your Flask app, create an ``OpenHeart`` instance and call ``OpenHeart.init_app()``.

.. code-block:: python

    from flask import Flask
    from flask_openheart import OpenHeart

    app = Flask(__name__)
    openheart = OpenHeart()
    openheart.init_app(app)

Add the ``openheart=True`` argument to any Flask endpoint.

.. code-block:: python

    @app.route("/foo/", openheart=True)
    def foo(self):
        return "bar"

The "/foo/" endpoint will be created as normal, but an additional "/openheart/foo/" endpoint will be created as well.
The OpenHeart endpoint handles all OpenHeart API requests related to "/foo/".

View/Submit Reactions
---------------------

Launch the Flask application:

.. code-block:: shell

    FLASK_APP=app:app flask run

To submit a reaction for "/foo/", you can make a POST request with ``curl`` to the corresponding OpenHeart API endpoint:

.. code-block:: shell

   curl -d '❤️' -X POST 'http://localhost:5000/openheart/foo/'

To view all the current reactions for "/foo/", you can make a GET request:

.. code-block:: shell

    curl 'http://localhost:5000/openheart/foo/'

Insert Reactions in Pages
-------------------------

Whenever a request is handled, if it is for an OpenHeart-enabled endpoint, Flask-OpenHeart will inject information into
``flask.request`` pertaining to this endpoint's reactions.

When generating HTML, you can use this to add information about reactions into your endpoint:

.. code-block:: python

    @app.route("/foo/", openheart=True)
    def foo(self):
        hearts_count = flask.request.openheart.reactions.get("❤️", 0)
        return "<p>Number of ❤️ reactions: {hearts_count}</p>"

Or, if you use templates:

.. code-block:: jinja

    {% set hearts_count = request.openheart.reactions.get("❤️", 0) %}
    <p>Number of ❤️ reactions: {{ hearts_count }}</p>

You can even render each reaction as a button and wrap the whole thing in an HTML form. This allows visitors to add
a reaction by clicking the button.

.. code-block:: jinja

    <form action="{{ request.openheart.post_url }}" method="POST" enctype="text/plain">
    {% for reaction, count in request.openheart.reactions.items() %}
      <button name="{{ reaction }}">{{ reaction }} ({{ count }})</button>
    {% endfor %}
    </form>

Endpoints with Arguments
------------------------

By default, Flask-OpenHeart stores all reactions for a given endpoint together with each other. However, a single
endpoint function might actually represent many distinct pages, in which case it may not be desireable for all of the
reactions to get grouped together.

For instance, it is common for a flask endpoint to be structured like:

.. code-block:: python

    @app.route("/articles/<id>/")
    def foo(id):
        article = get_article_from_database(id)
        if not article:
            abort(404)
        return render_template("article.html", article)

If OpenHeart were enabled for this endpoint, reactions submitted to *any* article will show up for *all* articles.

To avoid this, we can provide a slug function. The slug function takes all the same arguments as the endpoint function
and returns a unique ID. Flask-OpenHeart will append the slug to the endpoint name whenever it stores and fetches
reactions.

The slug function can also return ``None`` to indicate that nothing exists with the provided arguments. This causes
Flask-OpenHeart to reject all API calls with those arguments.

.. code-block:: python

    @app.route("/articles/<id>/", openheart=True)
    def foo(id):
        article = get_article_from_database(id)
        if not article:
            abort(404)
        return render_template("article.html", article)

    @foo.slug
    def foo_slug(id):
        if not article_exists_in_database(id):
            return None
        return id
