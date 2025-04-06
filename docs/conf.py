import os

# For the full list of built-in configuration values, see the Sphinx documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

project = "Flask-OpenHeart"
copyright = "2025, Woodrow Barlow"  # noqa: A001
author = "Woodrow Barlow"

extensions = [
    "sphinx.ext.autodoc",
    "sphinx_rtd_theme",
]

templates_path = ["_templates"]
exclude_patterns = []

html_theme = "sphinx_rtd_theme"
html_static_path = ["_static"]

html_baseurl = os.environ.get("READTHEDOCS_CANONICAL_URL", "/")
