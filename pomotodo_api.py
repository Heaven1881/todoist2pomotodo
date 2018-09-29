# coding:utf8
import requests


def get_all_todo(token, completed=False):
    try:
        return requests.get(
            'https://api.pomotodo.com/1/todos',
            headers={
                "Authorization": "token %s" % token
            }).json()
    except Exception as e:
        print e.message
    return []


def add_todo(token, description):
    try:
        return requests.post(
            "https://api.pomotodo.com/1/todos",
            data={
                "description": description
            },
            headers={
                "Authorization": "token %s" % token
            }
        ).json()
    except Exception as e:
        return {"message": e.message}
