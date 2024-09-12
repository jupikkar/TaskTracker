import argparse
import json
import os
import pathlib


RESOURCE_PATH = pathlib.Path.cwd() / 'res'
TASKS_JSON = RESOURCE_PATH / 'tasks.json'
            
def load_tasks():
    with open(TASKS_JSON) as f:
            tasks = json.load(f)
    return tasks

def create_task_json():
    RESOURCE_PATH.mkdir(exist_ok=True)
    empty_tasks = {'tasks': []}
    with open(TASKS_JSON, mode='x') as f:
        f.write(json.dumps(empty_tasks))

def get_args() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="TaskTracker", description="A simple app for tracking tasks")
    mutex_arg_group = parser.add_mutually_exclusive_group()
    mutex_arg_group.set_defaults(mode='insert')
    mutex_arg_group.add_argument('-a','--add', type=str)
    mutex_arg_group.add_argument('-u','--update', type=str)
    mutex_arg_group.add_argument('-d','--delete', type=str)
    mutex_arg_group.add_argument('-l','--list', choices=['all', 'done', 'todo', 'ongoing'])
    args = parser.parse_args()
    return args

def load_task_json():
    try:
        tasks = load_tasks()
    except FileNotFoundError:
        create_task_json()
        tasks = load_tasks()
    return tasks

def choose_action(args: argparse.Namespace):
    action, value = None, None
    if args.add:
        action = 'add'
        value = args.add
    elif args.update:
        action = 'update'
        value = args.update
    elif args.delete:
        action = 'delete'
        value = args.delete
    elif args.list:
        action = 'list'
        value = args.list
    return (action, value)


def main():
    args = get_args()
    tasks = load_task_json()
    action, value = choose_action(args)
    print(action)
    print(value)
    print(tasks)

if __name__ == "__main__":
    main()