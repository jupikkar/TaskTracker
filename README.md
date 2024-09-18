# Task Tracker

A simple app for saving and updating task lists.

## Specifications

Inspired by https://roadmap.sh/projects/task-tracker

## Requirements

A Python version at a minimum of 3.10 is required.

## Usage

python tasktracker.py -h will display available commands.

Example:
```
python tasktracker.py -a "Make a task."
Task Tracker: Task added successfully (ID: 1)

$ python tasktracker.py -l all
Task Tracker: ##### List of Tasks #####
Task Tracker: Task ID: 0, Task Status: done, Created: Wed Sep 18 11:04:07 2024, Last updated: Wed Sep 18 11:11:20 2024
Task Tracker: Task ID: 1, Task Status: todo, Created: Wed Sep 18 12:02:21 2024, Last updated: Wed Sep 18 12:02:21 2024
