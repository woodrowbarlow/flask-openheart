# Flask-OpenHeart

A [Flask](https://flask.palletsprojects.com/en/stable/) extension to add support for the [OpenHeart protocol](https://openheart.fyi/).

## Documentation

Full documentation is on [ReadTheDocs](https://flask-openheart.readthedocs.io/en/latest/).

## Development

depending on the tools you prefer, multiple development workflows are supported.

* if you prefer to use python tools directly via uv, see [`DEVELOPMENT.generic.md`](https://github.com/woodrowbarlow/flask-openheart/blob/main/DEVELOPMENT.generic.md).
* if you prefer to use containers via docker or podman, see [`DEVELOPMENT.containers.md`](https://github.com/woodrowbarlow/flask-openheart/blob/main/DEVELOPMENT.containers.md).
* if you prefer to use the vscode IDE with a devcontainer, see [`DEVELOPMENT.vscode.md`](https://github.com/woodrowbarlow/flask-openheart/blob/main/DEVELOPMENT.vscode.md).

## TODO

* [x] (infra) uv project/dependencies setup
* [x] (infra) module/folder structure
* [x] (infra) linter/formatter setup
* [x] (infra) dummy test cases (pytest)
* [x] (infra) dummy docs page
* [x] (infra) containers/compose support
* [x] (infra) reusable (optional) IDE setup (vscode)
* [x] (infra) developer documentation
* [x] (infra) pre-commit hooks
* [ ] (infra) type annotations? (pyright + ruff)
* [ ] (infra) test coverage reports?
* [ ] (infra) branch protections and PR workflows
* [ ] (infra) github issues?
* [ ] (infra) github actions?
* [ ] (infra) packaging for multiple python versions
* [ ] (infra) versioned releases
* [ ] (infra) hot-reloading "examples" module
* [ ] (infra) hot-reloading pytests webview?
* [ ] (infra) ide integration for hot-loading examples, docs, tests
