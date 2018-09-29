# coding=utf-8
import todoist_api
import pomotodo_api

TODOIST_TOKEN = 'xxxxx'
POMOTODO_TOKEN = 'xxxxx'

map_projects_by_id = {}
map_task_list_by_project_id = {}
pomotodo_desc_list = []


def get_project_name_by_id(project_id):
    return map_projects_by_id[project_id]['name']


def get_horizontal_task_name(project_id, order, indent, content):
    if indent == 1:
        return '#%s %s' % (get_project_name_by_id(project_id), content)

    # 获取task所属project的所有任务
    if project_id in map_task_list_by_project_id:
        tasks_in_project = map_task_list_by_project_id[project_id]
    else:
        tasks_in_project = todoist_api.get_active_tasks(TODOIST_TOKEN, project_id=project_id)
        if len(tasks_in_project) > 0:
            map_task_list_by_project_id[project_id] = tasks_in_project

    # 找到task的父task
    parent_task = None
    for task in tasks_in_project:
        if task['order'] < order and task['indent'] == indent - 1:
            if not parent_task:
                parent_task = task
            elif task['order'] > parent_task['order']:
                parent_task = task

    if parent_task:
        return '%s | %s' % (
            get_horizontal_task_name(project_id, parent_task['order'], parent_task['indent'], parent_task['content']),
            content)
    else:
        # 找不到父task，这应该是不可能的，这个条件下直接使用project名字
        return '#%s %s' % (get_project_name_by_id(project_id), content)


if __name__ == '__main__':

    print "[TODOIST] Downloading project list ..."
    projects = todoist_api.get_all_projects(TODOIST_TOKEN)
    print "[TODOIST] Downloading project list ... OK"

    # 构件索引
    for proj in projects:
        if 'id' in proj and 'name' in proj:
            map_projects_by_id[proj['id']] = proj

    print "[TODOIST] Downloading today's task ..."
    today_tasks = todoist_api.get_active_tasks(TODOIST_TOKEN, task_filter="(overdue|today)")
    print "[TODOIST] Downloading today's task ... OK"

    print "[POMOTODO] Downloading all todo ..."
    pomotodos = pomotodo_api.get_all_todo(POMOTODO_TOKEN)
    print "[POMOTODO] Downloading all todo ... OK"

    # 构件索引
    for pomotodo in pomotodos:
        pomotodo_desc_list += [pomotodo['description']]

    print "[   ] Finding new task and todo ..."
    if len(projects) > 0 and len(today_tasks):
        '''
        遍历每个task，获取其根据任务数拍扁后的任务名
        '''

        added_task = 0
        repeated_task = 0

        for task in today_tasks:
            # 当任务设置了优先级，才会同步到番茄土豆
            if task.get('priority', 0) > 1:
                todo_name = get_horizontal_task_name(task['project_id'], task['order'], task['indent'], task['content'])

                # 将todo中不存在的项添加到番茄土豆中
                if todo_name not in pomotodo_desc_list:
                    added_task += 1

                    result = pomotodo_api.add_todo(POMOTODO_TOKEN, todo_name)
                    if 'uuid' in result:
                        print "[ADDED  ]", "\t", todo_name
                    else:
                        print "[FAILED ]", "\t", todo_name
                else:
                    repeated_task += 1
                    print "[SKIPPED]", "\t", todo_name

        print "[   ] Add %d task(s), %d task(s) are skipped" % (added_task, repeated_task)
    else:
        print "[   ] Empty result!"
        print "[   ] Finding new task and todo ... OK"
