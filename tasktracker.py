import argparse
import datetime
import json
import logging
import os
import pathlib
import sys
import time
from typing import Tuple


RESOURCE_PATH = pathlib.Path.cwd() / 'res'
TASKS_JSON = RESOURCE_PATH / 'tasks.json'
LOGGER = logging.getLogger("Task Tracker")
            
def load_tasks_from_json():
    with open(TASKS_JSON) as f:
        tasks = json.load(f)
    return tasks

def create_task_json():
    RESOURCE_PATH.mkdir(exist_ok=True)
    empty_tasks = {'tasks': {}}
    with open(TASKS_JSON, mode='x') as f:
        f.write(json.dumps(empty_tasks))

def get_args() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="TaskTracker", description="A simple app for tracking tasks")
    mutex_arg_group = parser.add_mutually_exclusive_group()
    mutex_arg_group.set_defaults(mode='insert')
    mutex_arg_group.add_argument('-a','--add', type=str, help="Add a task. Usage: --add 'Description of task'")
    mutex_arg_group.add_argument('-u','--update', nargs='+', help="Update a task. Usage: --update <ID> <'Description of task'>")
    mutex_arg_group.add_argument('-r','--remove', type=str, help="Remove a task. Usage: --remove <ID>")
    mutex_arg_group.add_argument('-o','--ongoing', type=str, help="Mark a task as in-progress. Usage: --ongoing <ID>")
    mutex_arg_group.add_argument('-d','--done', type=str, help="Mark a task as done. Usage: --done <ID>")
    mutex_arg_group.add_argument('-l','--list', choices=['all', 'done', 'todo', 'ongoing'], help="List all tasks, or by status. Usage: --list all|done|ongoing|todo")
    args = parser.parse_args()
    return args

def load_tasks() -> dict[str]:
    try:
        tasks = load_tasks_from_json()
    except FileNotFoundError:
        create_task_json()
        tasks = load_tasks_from_json()
    return tasks["tasks"]

def save_tasks_to_json(tasks: list):
    task_list = {'tasks': tasks}
    with open(TASKS_JSON, mode='w') as f:
        json.dump(task_list, f, indent=2)

def choose_action(args: argparse.Namespace) -> Tuple[str, str | list]:
    action: str = ''
    value: str = ''
    if args.add:
        action = 'add'
        value = args.add
    elif args.update:
        action = 'update'
        value = args.update
    elif args.remove:
        action = 'remove'
        value = args.remove
    elif args.list:
        action = 'list'
        value = args.list
    else:
        # This should already be safeguarded by the mutex arg group, but safe is safe.
        action = 'unknown'
    return (action, value)

def get_new_task_id(tasks: dict):
    task_ids = [int(id) for id in tasks.keys()]
    if not task_ids:
        new_id = 0
    else:
        new_id = max(task_ids) + 1
    return new_id

def _current_time():
    return datetime.datetime.now(tz=datetime.timezone.utc).astimezone().isoformat()

def _add(value: str):
    tasks = load_tasks()
    new_id = get_new_task_id(tasks)
    creation_time = _current_time()
    new_task = {
        "description": value,
        "status": "todo",
        "createdAt": creation_time,
        "updatedAt": creation_time
    }
    tasks[new_id] = new_task
    save_tasks_to_json(tasks)
    LOGGER.info(f'Task added successfully (ID: {new_id})')    

def _update(value: list):
    try:
        task_id, new_task = _parse_update_values(value)
    except (IndexError, ValueError):
        LOGGER.error('Update takes exactly two values, Task ID (integer) and Task description (str)!')
        return
    tasks = load_tasks()
    try:
        _update_task(task_id, new_task, tasks)
    except KeyError:
        LOGGER.error('Task ID does not exist!')
    save_tasks_to_json(tasks)
    LOGGER.info(f'Task updated successfully (ID: {task_id}, Description: "{new_task}")') 

def _update_task(task_id, new_task, tasks):
    tasks[str(task_id)]["description"] = new_task
    tasks[str(task_id)]["updatedAt"] = _current_time()

def _parse_update_values(value):
    task_id = int(value[0])
    new_task = value[1]
    if type(task_id) != int or type(new_task) != str:
        raise IndexError
    return task_id,new_task

def _remove(value: str):
    tasks = load_tasks()
    try:
        del(tasks[value])
    except KeyError:
        LOGGER.error(f'Remove failed; ID {value} does not exist!')
        return
    save_tasks_to_json(tasks)
    LOGGER.info(f'Task removed successfully (ID: {value})') 

def _list(value: str):
    tasks = load_tasks()
    tasks_to_print = None
    if value == "all":
        tasks_to_print = [task for task in tasks.items()]
    else:
        tasks_to_print = [task for task in tasks.items() if task[1]["status"] == value]
    if tasks_to_print:
        LOGGER.info("##### List of Tasks #####")
        [_print_task(task) for task in tasks_to_print]
    else:
        LOGGER.info("No tasks to print!")

def _print_task(task: tuple):
    task_id = task[0]
    task = task[1]
    created = datetime.datetime.fromisoformat(task['createdAt'])
    updated = datetime.datetime.fromisoformat(task['updatedAt'])
    readable_created = created.strftime("%c")
    readable_updated = updated.strftime("%c")
    LOGGER.info(f"Task ID: {task_id}, Task Status: {task['status']}, Created: {readable_created}, Last updated: {readable_updated}")

def perform_action(action: str, value: str | list):
    match action:
        case 'add':
            _add(value)
        case 'update':
            _update(value)
        case 'remove':
            _remove(value)
        case 'list':
            _list(value)

def set_up_logging():
    logging.basicConfig(level=logging.INFO, format='%(name)s: %(message)s')
    LOGGER.debug('Started')

def main():
    set_up_logging()
    args = get_args()
    action, value = choose_action(args)
    perform_action(action, value)
    LOGGER.debug('Finished')

if __name__ == "__main__":
    main()