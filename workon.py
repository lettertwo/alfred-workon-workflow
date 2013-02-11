#!/usr/bin/env python
from lxml.etree import Element, SubElement, tostring
import os
import re

project_dir = os.path.expanduser('~/Projects')

attrs = ('uid', 'arg', 'type', 'valid', 'autocomplete')
els = ('title', 'subtitle', 'icon')

def serialize(project):
    path = os.path.join(project_dir, project)
    return {
        'title': project,
        'subtitle': path,
        'arg': path,
        'uid': path,
        'type': 'file',
    }

def find_projects(query='.*'):
    query = re.compile(r'%s' % query)
    return (n for n in next(os.walk(project_dir))[1] if query.search(n))

def list_projects(kw=None):
    items = Element('items')
    for i, project in enumerate(find_projects(kw)):
        item = SubElement(items, 'item')
        item.set('uid', '%d' % i)
        for k, v in serialize(project).items():
            if k in attrs:
                item.set(k, v)
            elif k in els:
                key = SubElement(item, k)
                key.text = v
    return tostring(items)


def get_project(path):

    return path



if __name__ == '__main__':
    print(list_projects('black'))
