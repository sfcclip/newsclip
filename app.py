#!/usr/bin/bpython
# -*- coding: utf-8 -*-

import os, pickle
from bottle import route, request, view, run, jinja2_template as template

@route('/')
def index():
    dirname = os.path.dirname(os.path.abspath(__file__))
    dump_file = os.path.normpath(os.path.join(dirname, './newclip.dump'))
    with open(dump_file, 'rb') as f:
        entries = pickle.load(f)

    queries = []
    for query in entries:
        queries.append(query)

    template_file = os.path.normpath(os.path.join(dirname, './index.j2'))
    return template(template_file, queries=queries, entries=entries)

run(host='localhost', port=3030, debug=True)
