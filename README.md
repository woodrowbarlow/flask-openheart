# Flask-OpenHeart

**Flask-OpenHeart** adds [OpenHeart][openheart] support to [Flask][flask] applications, providing a simple way for users
to react with emojis to Flask URLs.

Flask-OpenHeart can be installed from [PyPI][pypi]:

```shell
pip install flask-openheart
```

And initialized like a typical [Flask extension][flask-ext]:

```python
from flask import Flask
from flask_openheart import OpenHeart

app = Flask(__name__)
openheart = OpenHeart()
openheart.init_app(app)
```

To enable OpenHeart support for an endpoint, simply add `openheart=True`:

```python
@app.route("/foo/", openheart=True)
def foo(self):
    return "<p>hello, world</p>"
```

This creates a "/foo/" endpoint as normal. This *also* creates a
"/openheart/foo/" endpoint.

Users can react to "/foo/" by submitting a POST request to "/openheart/foo/"
containing any emoji. For example:

```shell
curl -d '❤️' -X POST 'http://localhost:5000/openheart/foo/'
```

Users can query the current reactions by submitting a GET request to
"/openheart/foo/". For example:

```shell
curl 'http://localhost:5000/openheart/foo/'
```

You can also easily add information about reactions into your endpoint:

```python
@app.route("/foo/", openheart=True)
def foo(self):
    hearts_count = flask.request.openheart.reactions["❤️"]
    return "<p>Number of ❤️ reactions: {hearts_count}</p>"
```

Full documentation for Flask-OpenHeart is available at [ReadTheDocs][readthedocs].

[pypi]: https://pypi.org/project/flask-openheart/
[readthedocs]: https://flask-openheart.readthedocs.io/
[openheart]: https://openheart.fyi/
[flask]: https://flask.palletsprojects.com/
[flask-ext]: https://flask.palletsprojects.com/en/stable/extensions/
