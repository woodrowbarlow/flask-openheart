## pre-requisites

install [git](https://git-scm.com/downloads).

install [uv](https://docs.astral.sh/uv/getting-started/installation/).

## get the code

```
git clone https://github.com/woodrowbarlow/flask-openheart.git
```

(or use ssh if preferred)

## (optional) pre-commit hooks

the pre-commit hooks will run linting checks before you commit, helping keep code clean.

```
uv run --dev just setup
```

## running examples

to serve all the examples at once:

```
uv run --dev just serve-examples
```

or to serve just a specific example:

```
# replace "basic" with the name of the example to run
uv run --dev just serve-example basic
```

then open http://localhost:5000 in your browser.

the server will detect file changes and reload automatically as you develop.

## building documentation

to build the docs:

```
uv run --dev just docs
```

the resulting files are in `docs/_build/html`.

alternatively, you can run a local docs server.

```
uv run --dev just serve-docs
```

then open http://localhost:8000 in your browser.

the server will detect file changes and reload automatically as you develop.

## running tests

```
uv run --dev just test
```

## linting checks

to run linter checks:

```
uv run --dev just lint
```

alternatively, to automatically fix as much as possible:

```
uv run --dev just lint-fix
```

note: if you set up the pre-commit hooks, lint-fix will be done automatically on each commit.
