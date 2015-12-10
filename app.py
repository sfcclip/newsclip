#!/usr/bin/bpython
# -*- coding: utf-8 -*-

import os, pickle
from bottle import route, request, view, run, jinja2_template as template

dirname = os.path.dirname(os.path.abspath(__file__))

def load_data():
    dump_file = os.path.normpath(os.path.join(dirname, './newsclip.dump'))
    with open(dump_file, 'rb') as f:
        entries = pickle.load(f)

    queries = []
    for query in entries:
        queries.append(query)

    return queries, entries

@route('/')
def index():
    queries, entries = load_data();
    template_file = os.path.normpath(os.path.join(dirname, './index.j2'))
    return template(template_file, queries=queries, entries=entries)

@route('/generate', method='POST')
def generate():
    urls = request.forms.getall('urls')
    print(urls)

    queries, entries = load_data()

    list = []
    for query in queries:
        list += [entry for entry in entries[query] if entry['link'] in urls]
    template_file = os.path.normpath(os.path.join(dirname, './generate.j2'))
    return template(template_file, entries=list)

run(host='localhost', port=3030, debug=True)
