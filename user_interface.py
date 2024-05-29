'''
This module deals with user interaction and anticupates error handeling
for invalid inputs. This level interacts with the buissness logic
module.
1. TaskManger class creates an interface for the user to interact with.
2. TaskManger class then holds functions for view task, add task, etc.
   these functions interact with the buissness logic module.
3. The module also interacts with the constants module for error
   handeling.
'''

import datetime

from buisness_logic import TaskService
from constants import DESCRIPTION_MAX_LENGTH, TITLE_MAX_LENGTH


class TaskManager:

    def __init__(self):  # Constructor to access TaskService
        self.task_service = TaskService()

    @staticmethod  # Static method for main menu
    def display_menu():
        print('''\nTask Management Application
    1. View Tasks
    2. Add Tasks
    3. Edit a Task
    4. Delete a Task
    5. Clear All Tasks
    6. Exit''')

    def run_task_manager(self):  # While loop to display main menu
        while True:
            self.display_menu()
            choice = input("Enter your choice: ")
            if choice == "1":
                self.view_tasks()
            elif choice == "2":
                self.add_task()
            elif choice == "3":
                self.edit_task()
            elif choice == "4":
                self.delete_task()
            elif choice == "5":
                self.task_service.clear_all_tasks()
            elif choice == "6":
                print("\nExiting the application. Goodbye!")
                return
            else:
                print("Invalid choice. Please try again.")

    def view_tasks(self):  # Display view tasks
        tasks = self.task_service.get_all_tasks()
        print("Active Tasks:")
        for idx, task in enumerate(tasks):
            print(f"{idx + 1}. {str(task)}")

    def add_task(self):  # Display edit task and error handle
        title = input("Enter Task title: ")
        description = input("Enter Task description: ")
        due_date_str = input("Enter Task Deadline (DD-MM-YYYY): ")
        try:
            due_date = datetime.datetime.strptime(due_date_str, "%d-%m-%Y")
            if (len(title) <= TITLE_MAX_LENGTH and
                    len(description) <= DESCRIPTION_MAX_LENGTH):
                if self.task_service.add_task(title, description, due_date):
                    print("Task added successfully!")
                else:
                    print("Task exceeds maximum length.")
            else:
                print("Title or description exceeds maximum length.")
        except ValueError:
            print("Invalid date format. Please use DD-MM-YYYY.")

    def edit_task(self):  # Display edit taska and error handle
        tasks = self.task_service.get_all_tasks()
        print("Tasks:")
        for idx, task in enumerate(tasks):
            print(f"{idx + 1}. {task.title}")
        try:  # Error handeling
            user_index = int(input(
                "Enter the index number you would like to edit: ")) - 1
            if 0 <= user_index < len(tasks):
                updated_title = input("Enter updated title: ")
                updated_description = input("Enter updated description: ")
                updated_due_date_str = input(
                    "Enter updated due date (DD-MM-YYYY): ")
                try:
                    updated_due_date = datetime.datetime.strptime(
                        updated_due_date_str, "%d-%m-%Y")
                    if (len(updated_title) <= TITLE_MAX_LENGTH and
                            len(updated_description) <=
                            DESCRIPTION_MAX_LENGTH):
                        print(self.task_service.edit_task(user_index,
                                                          updated_title,
                                                          updated_description,
                                                          updated_due_date))
                    else:
                        print("Updated title or description "
                              "exceeds maximum length.")
                except ValueError:
                    print("Invalid date format. Please use DD-MM-YYYY.")
            else:
                print("Invalid index. Task not updated.")
        except ValueError:
            print("Invalid input. Please enter a valid index.")

    def delete_task(self):  # Delete task and error handle.
        tasks = self.task_service.get_all_tasks()
        print("Tasks:")
        for idx, task in enumerate(tasks):
            print(f"{idx + 1}. {task.title}")
        while True:
            user_choose = int(input("Enter the index number you would "
                                    "like to delete: ")) - 1
            if 0 <= user_choose < len(tasks):
                result = self.task_service.delete_task(user_choose)
                print(result)
                break
            else:
                print("Invalid index. Returning to the main menu.")
                break
