#!/usr/bin/env python
from lxml.etree import Element, SubElement, tostring
import os
import re

project_dir = os.path.expanduser('~/Projects')

def serialize(project):
    return {
        'title': project,
        'subtitle': 'subtitle here'
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
            key = SubElement(item, k)
            key.text = v
    return tostring(items)


if __name__ == '__main__':
    print(list_projects('black'))
