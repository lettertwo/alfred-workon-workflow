#!/usr/bin/env python
import sys
import os
import re
import subprocess

sys.path.append(os.path.join(os.path.dirname(__file__), 'alp'))
import alp

settings = alp.Settings()

if settings.get('project_types') is None:
    settings.set(project_types={
        ".sublime-workspace": {
            "cmd": "/usr/local/bin/subl",
        },
    })


def get_project_title(project_path):
    return os.path.splitext(os.path.basename(project_path))[0]


def serialize_project(project_path, project_type):
    project = dict(
        title=get_project_title(project_path),
        subtitle=project_path,
        arg=project_path,
        uid=project_path,
    )
    project.update(settings.get('project_types')[project_type])
    return project


def find_projects(query=None):
    if query is None:
        query = '.*'
    query = re.compile(r'%s' % query, re.IGNORECASE)
    for t in settings.get('project_types').keys():
        type_query = re.compile(r'.+%s$' % t)
        for p in alp.find(t):
            if type_query.match(p) and query.search(p):
                yield serialize_project(p, t)


def list_projects(kw=None):
    feedback = []
    for project in find_projects(kw):
        meta = {'valid': True}
        meta.update(**project)
        feedback.append(alp.Item(**meta))
    return alp.feedback(feedback)


def open_project(project_path):
    title = get_project_title(project_path)
    path = os.path.dirname(project_path)
    if 'project' in next(os.walk(path))[1]:
        path = os.path.join(path, 'project')

    subprocess.call(['osascript', 'iterm.applescript', title, path],
                    close_fds=True)
