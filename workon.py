#!/usr/bin/env python
import sys
import os
import time
import re
import subprocess
import cPickle
import multiprocessing

sys.path.append(os.path.join(os.path.dirname(__file__), 'alp'))
import alp

settings = alp.Settings()

projects_cache = alp.cache(join='projects.cache')

if settings.get('project_types') is None:
    settings.set(project_types=(
        ".sublime-workspace",
    ))


def get_project_title(project_path):
    return os.path.splitext(os.path.basename(project_path))[0]


def serialize_project(project_path):
    meta = dict(
        title=get_project_title(project_path),
        subtitle=project_path,
        arg=project_path,
        uid=project_path,
        valid=True,
    )
    return dict(meta=meta, feedback=alp.Item(**meta))


def update_project_list_cache():
    results = get_project_list()
    with open(projects_cache, 'wb') as f:
        cPickle.dump(results, f)


def get_project_list_cached():
    try:
        with open(projects_cache, 'rb') as f:
            results = cPickle.load(f)
    except (IOError, EOFError):
        results = get_project_list()

    try:
        needs_update = os.path.getmtime(projects_cache) < time.time() - 60
    except OSError:
        needs_update = True

    if needs_update:
        multiprocessing.Process(target=update_project_list_cache).run()

    return results


def get_project_list():
    projects = []
    for t in settings.get('project_types'):
        type_query = re.compile(r'.+%s$' % t)
        for p in alp.find(t):
            if type_query.match(p):
                projects.append(serialize_project(p))
    return projects


def filter_projects(query=None):
    projects = get_project_list_cached()
    if query:
        query = re.compile(r'%s' % query, re.IGNORECASE)
        projects = (project for project in projects
                    if query.search(project['meta']['title']))
    return projects


def list_projects(kw=None):
    feedback = []
    for project in filter_projects(kw):
        feedback.append(project['feedback'])
    return alp.feedback(feedback)


def open_project(project_path):
    title = get_project_title(project_path)
    path = os.path.dirname(project_path)
    if 'project' in next(os.walk(path))[1]:
        path = os.path.join(path, 'project')

    subprocess.call(['osascript', 'iterm.applescript', title, path],
                    close_fds=True)
