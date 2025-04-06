lint:
    ruff check
    ruff format --check
lint-fix:
    ruff check --fix
    ruff format
serve-example target:
    flask --app examples.{{ target }} run
serve-examples:
    flask --app examples run
serve-docs:
    sphinx-autobuild docs/ docs/_build/html
setup:
    pre-commit install
docs:
    sphinx-build docs/ docs/_build/html
test:
    pytest
