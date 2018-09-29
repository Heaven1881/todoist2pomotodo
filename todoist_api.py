# coding:utf8
import requests

DEFAULT_LANG = None


def get_all_projects(token):
    try:
        return requests.get(
            "https://beta.todoist.com/API/v8/projects",
            headers={
                "Authorization": "Bearer %s" % token
            }).json()
    except Exception as e:
        print e.message
    return []


def get_active_tasks(token, project_id=None, label_id=None, task_filter=None, lang=None):
    try:
        return requests.get(
            "https://beta.todoist.com/API/v8/tasks",
            params={
                "project_id": project_id,
                "label_id": label_id,
                "filter": task_filter,
                "lang": lang
            },
            headers={
                "Authorization": "Bearer %s" % token
            }).json()
    except Exception as e:
        print e.message
    return []
