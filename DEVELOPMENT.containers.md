## pre-requisites

install [docker](https://docs.docker.com/engine/install/) (or [podman](https://podman.io/docs/installation)).

install [docker compose](https://docs.docker.com/compose/) (or [podman compose](https://docs.podman.io/en/latest/markdown/podman-compose.1.html)).

note: this doc assumes docker. if you are using podman, replace `docker` with `podman` throughout.

## get the code

```
git clone https://github.com/woodrowbarlow/flask-openheart.git
```

(or use ssh if preferred)

## running examples

to serve all the examples at once:

```
docker compose up --watch serve-examples
```

or to serve just a specific example:

```
# replace "basic" with the name of the example to run
docker compose up --watch -e FLASK_APP=examples.basic serve-examples
```

then open http://localhost:5000 in your browser.

the server will detect file changes and reload automatically as you develop.

## building documentation

to build the docs:

```
docker compose -f compose.util.yaml run --rm docs
```

the resulting files are in `docs/_build/html`.

alternatively, you can run a local docs server.

```
docker compose up --watch serve-docs
```

then open http://localhost:8000 in your browser.

the server will detect file changes and reload automatically as you develop.

## running tests

```
docker compose -f compose.util.yaml run --rm test
```

## linting checks

to run linter checks:

```
docker compose -f compose.util.yaml run --rm lint
```

alternatively, to automatically fix as much as possible:

```
docker compose -f compose.util.yaml run --rm lint-fix
```
