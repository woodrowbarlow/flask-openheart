"""The basic example shows the simplest way to add OpenHeart support to a Flask page."""

from flask import Flask, request

from flask_openheart import OpenHeartExtension


def create_app():
    """Create a Flask application instance and initialize the OpenHeart extension."""
    app = Flask(__name__)

    openheart = OpenHeartExtension()
    openheart.init_app(app)

    return app


app = create_app()


def make_footer():
    """A short html footer containing instructions for using OpenHeart reactions."""
    reactions_url = app.url_for(f"openheart.{request.endpoint}", _external=True, **request.args)
    return f"""<hr />
    <p>
        This page supports emoji-based reactions via the
        <a href="https://openheart.fyi/" target="_blank">OpenHeart protocol</a>!
    </p>
    <p>
        To view reactions via the command-line, try:
    </p>
    <pre><code>curl '{reactions_url}'</code></pre>
    <p>
        To submit a reaction via the command-line, try:
    </p>
    <pre><code>curl -d '❤️' -X POST '{reactions_url}'</code></pre>
    """


@app.route("/", openheart=True)
def index():
    """A basic Flask endpoint."""
    return f"""<h1>index</h1>
    <ul>
        <li><a href="{app.url_for("foo")}">foo</a></li>
        <li><a href="{app.url_for("bar")}">bar</a></li>
    </ul>
    """ + make_footer()


@app.route("/foo/", openheart=True)
def foo():
    """A basic Flask endpoint."""
    return f"""<h1>foo</h1>
    <p><a href="{app.url_for("index")}">back to index</a></p>
    """ + make_footer()


@app.route("/bar/")
def bar():
    """A basic Flask endpoint."""
    return f"""<h1>bar</h1>
    <p><a href="{app.url_for("index")}">back to index</a></p>
    <hr />
    <p>OpenHeart reactions are not supported on this page.</p>
    """
