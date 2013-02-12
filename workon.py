#!/usr/bin/env python
import PyAl
import os
import re
import subprocess

project_types = {
    '.sublime-workspace': {
        'cmd': '/usr/local/bin/subl',
    },
    # '.tmproj': {
    #     'cmd': 'mate',
    # },
}

def get_project_title(project_path):
    return os.path.splitext(os.path.basename(project_path))[0]

def serialize_project(project_path, project_type):
    project = dict(
        title=get_project_title(project_path),
        subtitle=project_path,
        arg=project_path,
        uid=project_path,
    )
    project.update(project_types[project_type])
    return project

def find_projects(query='.*'):
    query = re.compile(r'%s' % query, re.IGNORECASE)
    for t in project_types.keys():
        type_query = re.compile(r'.+%s$' % t)
        for p in PyAl.find(t):
            if type_query.match(p) and query.search(p):
                yield serialize_project(p, t)

def list_projects(kw=None):
    feedback = PyAl.Feedback()
    for project in find_projects(kw):
        meta = {'valid': True}
        meta.update(**project)
        feedback.add(PyAl.Item(**meta))
    return feedback

def open_project(project_path):
    title = get_project_title(project_path)
    path = os.path.dirname(project_path)
    if 'project' in next(os.walk(path))[1]:
        path = os.path.join(path, 'project')

    p = subprocess.call(['osascript', 'iterm.applescript', title, path], close_fds=True)


if __name__ == '__main__':
    open_project('/Users/ede/Projects/wall.digitalrealty.loc/wall.digitalrealty.sublime-project')
