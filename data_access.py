'''
This module deals with the database level of the Task Manager App.
1. TASK CLASS creates the blueprint for how tasks are created.
2. STR METHOD then creates a format for how tasks are displayed
   in a user friendly way.
3. TASK REPOSITORY holds functions for creating a database for the app
   using IO operations and saves them to a .txt file.

'''

import os.path
import datetime

from config import FILENAME
from utilities import format_date


class Task:

    def __init__(self, title, description, date_due):  # Constructor
        self.title = title  # Atributes
        self.description = description
        self.date_created = datetime.datetime.now()
        self.date_due = date_due

    def __str__(self):  # String method to display tasks
        return (
            f"Title: {self.title}\n Description: {self.description}\n "
            f"Due Date: {self.date_due}      Created at: {self.date_created}\n"
            )


class TaskRepository:
    def __init__(self, filename=FILENAME):  # Creates a .txt file
        self.filename = filename
        if not os.path.exists(filename):
            with open(filename, "w"):
                pass

    def get_tasks(self):  # Retrives all tasks and strips all format
        tasks = []
        with open(self.filename, "r") as file:
            lines = file.readlines()
            for line in lines:
                task_info = line.strip().split("|")
                title = task_info[0].strip()
                description = task_info[1].strip()
                due_date = datetime.datetime.strptime(
                    task_info[2].strip(), "%d-%m-%Y")
                created_at = datetime.datetime.strptime(
                    task_info[3].strip(), "%d-%m-%Y %H:%M:%S")
                task = Task(title, description, due_date)
                task.date_created = created_at
                tasks.append(task)
        return tasks

    def save_task(self, task):  # Saves tasks and formates to .txt file
        timestamp = format_date(datetime.datetime.now())
        formatted_due_date = task.date_due.strftime("%d-%m-%Y")
        with open(self.filename, "a") as file:
            file.write(f"{task.title} | {task.description} | "
                       f"{formatted_due_date} | {timestamp}\n")

    def save_updated_tasks(self, tasks):  # edits a task
        with open(self.filename, "w") as file:
            for task in tasks:  # iterates file and updates
                formatted_due_date = task.date_due.strftime("%d-%m-%Y")
                formatted_created_at = task.date_created.strftime(
                    "%d-%m-%Y %H:%M:%S")
                file.write(f"{task.title} | {task.description} | "
                           f"{formatted_due_date} | {formatted_created_at}\n")

    def clear_task_repo(self):  # Deletes .txt file
        os.remove(self.filename)
