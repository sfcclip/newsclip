#!/usr/bin/python
# -*- coding: utf-8 -*-

import pickle
from bottle import route, request, view, run, jinja2_template as template

@route('/')
def index():
    with open('newsclip.dump', 'rb') as f:
        entries = pickle.load(f)

    queries = []
    for query in entries:
        queries.append(query)

    return template('./index.j2', queries=queries, entries=entries)

run(host='localhost', port=8080, debug=True, reloader=True)
