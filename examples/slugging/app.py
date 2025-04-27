"""The slugging example shows how to control which pages are treated as distinct."""

from flask import Flask, abort, render_template

from flask_openheart import OpenHeart

from .data import pages  # a dummy faux-database for this example


def create_app():
    """Create a Flask application instance and initialize the OpenHeart extension."""
    app = Flask(__name__)

    openheart = OpenHeart()
    openheart.init_app(app)

    return app


app = create_app()


@app.route("/")
def index():
    """A Flask endpoint that renders a listing of all sub-pages."""
    return render_template("index.html", pages=dict(enumerate(pages)))


@app.route("/page/<int:page_id>/", openheart=True)
def page(page_id):
    """A Flask endpoint that renders a page by ID.

    Args:
        page_id: The page id.
    """
    if page_id >= len(pages):
        abort(404)
    return render_template("page.html", **pages[page_id])


@page.slug
def page_slug(page_id):
    """A slug function to disambiguate each page represented by the 'page' endpoint.

    By default, Flask-OpenHeart stores all reactions by endpoint name. Since all pages are being served under a single
    endpoint function, that means all reactions would (by default) get shared among all pages. This slug function is
    used by Flask-OpenHeart in order to store reactions for each page distinctly, rather than grouping by endpoint.

    Slug functions have the same function signature (accept the same arguments) as the corresponding endpoint function.

    Args:
        page_id: The page id.

    Returns:
        A unique slug for each page. This will be cast to a string by Flask-OpenHeart.
    """
    if page_id >= len(pages):
        # if we return a valid slug, then the page is "reactable" even if the page itself causes a 404 error.
        # the slug function can return None to indicate that the OpenHeart endpoint should also return 404.
        return None
    return page_id
