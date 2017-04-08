#!/usr/bin/python
# -*- coding: utf-8 -*-

import os, pickle
from bottle import route, request, view, run, jinja2_template as template

dirname = os.path.normpath(os.path.dirname(os.path.abspath(__file__)))

def load_data():
    dump_file = os.path.join(dirname, 'newsclip.dump')
    with open(dump_file, 'rb') as f:
        entries = pickle.load(f)
    return entries

@route('/')
def index():
    entries = load_data();
    print(os.path.join(os.path.dirname(__file__), 'index.j2'))
    return template(os.path.join(os.path.dirname(__file__), 'index.j2'), queries=entries.keys(), entries=entries)

@route('/generate', method='POST')
def generate():
    entries = load_data()
    uuids = request.forms.getall('uuids')
    list = [entry for query in entries.keys() for entry in entries[query] if entry['uuid'] in uuids]
    return template(os.path.join(os.path.dirname(__file__), 'generate.j2'), entries=list)

port = os.environ['PORT'] if 'PORT' in os.environ else 8080
run(host='localhost', port=port, debug=True)
