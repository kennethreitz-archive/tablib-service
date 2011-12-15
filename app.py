# -*- coding: utf-8 -*-

"""
tablib-service
~~~~~~~~~~~~~~

This is a simple web service for converting tabular datasets.
"""

from collections import OrderedDict

import tablib
from flask import Flask, request, jsonify


app = Flask(__name__)
app.debug = True

@app.route('/')
def index():

    d = {
        'resources': {
            '/:input/:output': 'POST. Converts request body from input to output formats.'
        },
        'formats': {
            'input': ['csv', 'tsv', 'json', 'yaml'],
            'output': ['csv', 'tsv', 'json', 'yaml', 'xls', 'xlsx', 'ods', 'html']
        },
        'errors': {
            406: 'The data you provided was invalid.',
            500: 'The server cannot convert your content.'
        },
        'source': 'https://github.com/kennethreitz/tablib-service'
    }
    return jsonify(d)


@app.route('/<f_from>/<f_to>', methods=['POST',])
def to_csv(f_from, f_to):
    d = tablib.Dataset()

    try:
        setattr(d, f_from, request.data)
    except Exception:
        return ':-/\n', 406


    try:
        result = getattr(d, f_to)
    except Exception:
        return ':-(\n', 500

    return result


if __name__ == '__main__':
    app.run()