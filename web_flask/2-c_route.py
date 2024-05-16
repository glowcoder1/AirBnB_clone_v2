#!/usr/bin/python3
"""
starts a Flask application
"""

from flask import Flask
app = Flask(__name__)
app.url_map.strict_slashes = False


@app.route('/')
def index():
    """handles home path"""
    return 'Hello HBNB!'


@app.route('/hbnb')
def hbnb():
    """handles /hbnb path"""
    return 'HBNB'


@app.route('/c/<text>')
def c_with_text(text):
    """handles /c path"""
    return 'C {}'.format(text.replace("_", " "))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5000')
