## pre-requisites

install [vscode](https://code.visualstudio.com/download).

install the [dev containers](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers) extension.

## get the code

```
git clone https://github.com/woodrowbarlow/flask-openheart.git
```

(or use ssh if preferred)

## ide configuration

file -> open folder -> (select this project folder)

ctrl + shift + p -> "Reopen in Container"

once finished, the bottom-left should show "Dev Container: OpenHeart-Flask".

all following commands in this doc should be executed in the vscode terminal, while connected to the dev container.

to open a new vscode terminal:

ctrl + shift + p -> "Create new Terminal"

## running examples

to serve all the examples at once:

```
just serve-examples
```

or to serve just a specific example:

```
# replace "basic" with the name of the example to run
just serve-example basic
```

then open http://localhost:5000 in your browser.

the server will detect file changes and reload automatically as you develop.

## building documentation

to build the docs:

```
just docs
```

the resulting files are in `docs/_build/html`.

alternatively, you can run a local docs server.

```
just serve-docs
```

then open http://localhost:8000 in your browser.

the server will detect file changes and reload automatically as you develop.

## running tests

```
just test
```

Or use the "Testing" tab on the left bar in vscode, then click "run tests".

## linting checks

to run linter checks:

```
just lint
```

alternatively, to automatically fix as much as possible:

```
just lint-fix
```

the lint-fix step will get run each time you save a file and before each commit.
