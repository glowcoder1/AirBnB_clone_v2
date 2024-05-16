#!/usr/bin/python3
"""
starts a Flask application
"""

from flask import Flask, render_template
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


@app.route('/python', defaults={"text": "is cool"})
@app.route('/python/<text>')
def py_with_text(text):
    """handles /python path"""
    return 'Python {}'.format(text.replace("_", " "))


@app.route('/number/<int:n>')
def is_number(n):
    """handles /number path"""
    return '{} is a number'.format(n)


@app.route('/number_template/<int:n>')
def number_temp(n):
    """handles /number_template path"""
    return render_template("5-number.html", number=n)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5000')
