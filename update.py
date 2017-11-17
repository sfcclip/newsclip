#!/usr/bin/python
# -*- coding: utf-8 -*-

import os, pickle, feedparser, urllib
from uuid import uuid1
from datetime import datetime

def format_date(date_str):
    date = datetime.strptime(date_str, "%a, %d %b %Y %H:%M:%S %Z")
    return datetime.strftime(date, '%Y年%m月%d日').decode('utf-8')

def get_original_url(google_url):
    return google_url.split('&url=')[-1]

def main():
    endpoint = 'https://news.google.com/news/rss/search/section/q/-CLIP+%s?ned=jp&gl=JP&hl=ja'

    print('Loading queries...')
    dirname = os.path.dirname(os.path.abspath(__file__))
    query_file = os.path.normpath(os.path.join(dirname, './queries.txt'))
    with open(query_file, 'r') as f:
        queries = [query.strip() for query in f.readlines() if len(query.strip()) > 0]

    entries = {}
    for query in queries:
        print('Fetching news for about "' + query + '"')
        url = endpoint % urllib.quote(query)
        feed = feedparser.parse(url)
        entries[query] = []
        for entry in feed['entries']:
            entries[query].append({
                'uuid'  : str(uuid1()),
                'title' : entry['title'],
                'link'  : get_original_url(entry['link']),
                'date'  : format_date(entry['published'])
            })

    dump_file = os.path.normpath(os.path.join(dirname, './newsclip.dump'))
    with open(dump_file, 'wb') as f:
        pickle.dump(entries, f)

    print('Done.')

if __name__ == '__main__':
    main()
