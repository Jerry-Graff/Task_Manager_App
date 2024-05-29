'''
This module acts as go between between our database and user interaface
to mask the behind scenes fuctiions and actions of the app.
1. TaskService class interacts with the database to add, update and
   delete user requests.
2. It also tries to deal with any invalid input that might have made it
   through.
'''

from data_access import TaskRepository, Task
from config import FILENAME
from constants import DESCRIPTION_MAX_LENGTH, TITLE_MAX_LENGTH


class TaskService:
    def __init__(self):  # Constructor to access database
        self.task_repository = TaskRepository(FILENAME)

    def get_all_tasks(self):  # Get tasks from database
        return self.task_repository.get_tasks()

    def add_task(self, title, description, due_date):
        if (len(title) <= TITLE_MAX_LENGTH
                and len(description) <= DESCRIPTION_MAX_LENGTH):
            task = Task(title, description, due_date)
            self.task_repository.save_task(task)
            return True
        else:
            return False

    def edit_task(self, index, updated_title,  # Edit task in database
                  updated_description, updated_due_date):
        tasks = self.task_repository.get_tasks()
        if 0 <= index < len(tasks):
            task = tasks[index]
            task.title = updated_title
            task.description = updated_description
            task.due_date = updated_due_date
            self.task_repository.save_updated_tasks(tasks)
            return f"Task at index {index + 1} updated successfully."
        else:
            return "Invalid index. Task not updated."  # Catch errors

    def delete_task(self, index):  # Delete task from database
        tasks = self.task_repository.get_tasks()
        if 0 <= index < len(tasks):
            del tasks[index]
            self.task_repository.save_updated_tasks(tasks)
            return f"Task at index {index + 1} deleted successfully."
        else:
            return "Invalid index. Task not deleted."

    def clear_all_tasks(self):  # Clear repository
        self.task_repository.clear_task_repo()
