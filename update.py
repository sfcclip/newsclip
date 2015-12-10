#!/usr/bin/python
# -*- coding: utf-8 -*-

import os, pickle, feedparser, urllib
from datetime import datetime

def format_date(date_str):
    date = datetime.strptime(date_str, "%a, %d %b %Y %H:%M:%S %Z")
    return datetime.strftime(date, '%Y年%m月%d日').decode('utf-8')

def main():
    endpoint = 'http://news.google.com/news?hl=ja&ned=us&ie=UTF-8&oe=UTF-8&output=rss&q=-CLIP+'

    print('Loading queries...')
    dirname = os.path.dirname(os.path.abspath(__file__))
    query_file = os.path.normpath(os.path.join(dirname, './queries.txt'))
    with open(query_file, 'r') as f:
        queries = [query.strip() for query in f.readlines() if len(query.strip()) > 0]

    entries = {}
    for query in queries:
        print('Fetching news for about "' + query + '"')
        url = endpoint + urllib.quote(query)
        feed = feedparser.parse(url)
        entries[query] = []
        for entry in feed['entries']:
            components = entry['title'].split(' - ')
            source = components.pop()
            title = ' - '.join(components)
            entries[query].append({
                'title': title,
                'link': entry['link'],
                'date': format_date(entry['published']),
                'source': source
            })

    dump_file = os.path.normpath(os.path.join(dirname, './newsclip.dump'))
    with open(dump_file, 'wb') as f:
        pickle.dump(entries, f)

    print('Done.')

if __name__ == '__main__':
    main()
