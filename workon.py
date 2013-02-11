#!/usr/bin/env python
import PyAl
import os
import re

project_dir = os.path.expanduser('~/Projects')

def find_projects(query='.*'):
    query = re.compile(r'%s' % query)
    return ((n, os.path.join(project_dir, n))
            for n in next(os.walk(project_dir))[1] if query.search(n))

def list_projects(kw=None):
    feedback = PyAl.Feedback()
    for project_name, project_path in find_projects(kw):
        feedback.add(PyAl.Item(
            title=project_name,
            subtitle=project_path,
            arg=project_path,
            uid=project_path,
            valid=True,
        ))
    return feedback


def get_project(path):
    return path

if __name__ == '__main__':
    print(list_projects('black'))
