# Import the os module for interacting with the operating system
import os

# Import datetime and date classes for handling date and time operations
from datetime import datetime, date

# Import Fore and Style from colorama for terminal text color formatting
from colorama import Fore, Style

# Names constanta for date_time format
DATETIME_STRING_FORMAT = "%d-%m-%Y"


# ANSI escape codes for text color
class Colors:
    RESET = '\033[0m'
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    PURPLE = '\033[95m'
    CYAN = '\033[96m'


''' Creates function to create txt file for keeping user's data,
if doesn't exist.
If file exists, reading user data.''' 
def read_user_data():
    # Checks if "user.txt" file exists, if not, 
    # creates it with default admin user
    if not os.path.exists("user.txt"):
        with open("user.txt", "w") as default_file:
            default_file.write("admin;password")

    # Reads user data from "user.txt" file
    with open("user.txt", 'r') as user_file:
        user_data = user_file.read().split("\n")

    # Initializes dictionary to store username-password pairs
    username_password = {}

    # Checks if any user data is available
    if user_data[0].strip():  
        # Iterates over each line of user data
        for user in user_data:
            username, password = user.split(';')
            # Stores username-password pair in the dictionary
            username_password[username] = password

    # If no user data is available, creates admin data by default
    else:
        username_password = {'admin': 'password'}

    return username_password


# Creates function to login
def login(username_password):
    # Initializes variables
    logged_in = False
    curr_user = ""
    
    # Loop until user is logged in
    while not logged_in:
        # Prompts user for username
        print(Colors.PURPLE + "LOGIN" + Colors.RESET)
        curr_user = input(Colors.YELLOW + "Username: " + Colors.RESET)
        
        # Checks if username exists
        if curr_user not in username_password.keys():
            print(Colors.RED + "User does not exist" + Colors.RESET)
            continue
        
        # Prompts user for password
        curr_pass = input(Colors.YELLOW + "Password: " + Colors.RESET)
        
        # Validates password
        if username_password[curr_user] != curr_pass:
            print(Colors.RED + "Wrong password" + Colors.RESET)
            continue
        
        # Successful login
        else:
            print(Colors.GREEN + "Login Successful!" + Colors.RESET)
            logged_in = True

    return curr_user


# Creates function to register users
def register_user(username_password):
    new_username = input(Colors.YELLOW + "New Username: " 
                         + Colors.RESET)

    # Checks if the username already exists
    if new_username in username_password:
        print(Colors.RED + "User already exists" 
              + Colors.RESET)
        return
    
    # Asks for the new password and confirms it
    new_password = input(Colors.YELLOW + "New Password: "
                          + Colors.RESET)
    confirm_password = input(Colors.YELLOW + "Confirm Password: " 
                             + Colors.RESET)

    # If passwords match, adds the new user and updates the user file
    if new_password == confirm_password:
        print(Colors.GREEN + "New user added" + Colors.RESET)
        username_password[new_username] = new_password
        
        # Writes the updated user data to the user file
        with open("user.txt", "w") as out_file:

            # Initializes empty list to store user's data
            user_data = []

            # Iterates through all users in the user.txt
            for username in username_password:
                # Appends new user to the list
                user_data.append(
                    f"{username};{username_password[username]}")
            # Joins user data to the file    
            out_file.write("\n".join(user_data))

    # If passwords don't match, displays an error message
    else:
        print(Colors.RED + "Passwords do not match" + Colors.RESET)


# Creates function to delete users
def delete_user(username_password, task_list):
    # Prompts for the username to be deleted
    username_to_delete = input(Colors.YELLOW 
    + "Enter the username you want to delete: "
    + Colors.RESET)

    # Checks if the current user is admin & enhance admin's rights
    if curr_user != 'admin':
        print(Colors.RED + "Users can be deleted by the admin only."
              + Colors.RESET)
        return

    # Prevents deletion of the admin user
    if username_to_delete == 'admin':
        print(Colors.RED + "Cannot delete the admin user." + Colors.RESET)
        return

    # Deletes the user if found in the username_password dictionary
    if username_to_delete in username_password:
        # Prompts user to confirm deletion
        delete_user_option = input(Colors.YELLOW 
        + f"Do you want delete {username_to_delete} (y/n):" + Colors.RESET)

        if delete_user_option == 'y':
            del username_password[username_to_delete]
        else:
            return

        # Updates the user.txt file with the 
        # modified username_password dictionary
        with open("user.txt", "w") as out_file:
            user_data = [
            f"{username};{password}" \
            for username, password in username_password.items()]
            
            out_file.write("\n".join(user_data))

        print(Colors.GREEN + f"User '{username_to_delete}' deleted successfully." 
        + Colors.RESET)

        # Marks tasks as deleted if user was associated with them
        for task in task_list:
            if task['username'] == username_to_delete:
                task['user_deleted'] = True

        # Handles the case where tasks.txt does not exist
        try:
            task_list = read_tasks_from_file("tasks.txt")

        except FileNotFoundError:
            # If tasks.txt does not exist, print a message and return
            print(Colors.RED + "Tasks file not found. No tasks to delete." 
            + Colors.RESET)
            return
        
        # Updates the tasks file with the modified task_list
        update_task_in_file(task_list, task)

    else:
        # Prints message if the user to be deleted is not found
        print(Colors.RED + f"User '{username_to_delete}' not found."
              + Colors.RESET)


# Creates function to create tasks for users
def add_task(task_list, username_password):
    task_username = input(Colors.YELLOW + "Name of person assigned to task: " 
    + Colors.RESET)

    # Checks if the entered username exists
    if task_username not in username_password.keys():
        print(Colors.RED + "User does not exist. Please enter a valid username" 
        + Colors.RESET)
        return

    # Prompts user for Title & Description 
    task_title = input(Colors.YELLOW + "Title of Task: " + Colors.RESET)
    task_description = input(Colors.YELLOW + "Description of Task: " 
                             + Colors.RESET)

    # Prompts the user for the due date until a valid date is entered
    while True:
        try:
            task_due_date = input(Colors.YELLOW 
            + "Due date of task (DD-MM-YYYY): " 
            + Colors.RESET)

            due_date_time = datetime.strptime(
            task_due_date, DATETIME_STRING_FORMAT)

            # Checks if the due date is in the past
            if due_date_time.date() < date.today():
                print(Colors.RED + "Sorry, you can't add overdue task." 
                + Colors.RESET)
                continue
            break

        except ValueError:
            print(Colors.RED 
            + "Invalid datetime format. Please use the format specified" 
            + Colors.RESET)

    curr_date = date.today()  # Declares current date = today

    # Creates a new task dictionary
    new_task = {
        "username": task_username,
        "title": task_title,
        "description": task_description,
        "due_date": due_date_time,
        "assigned_date": curr_date,
        "completed": False
    }

    # Appends the new task to the task list
    task_list.append(new_task)
    with open("tasks.txt", "w") as task_file:
        task_list_to_write = []
        
        # Writes the updated task list to the tasks.txt file
        for t in task_list:
            # Converts task attributes to string and joins them with semicolon
            str_attrs = [
                t['username'],
                t['title'],
                t['description'],
                t['due_date'].strftime(DATETIME_STRING_FORMAT),
                t['assigned_date'].strftime(DATETIME_STRING_FORMAT),
                "Yes" if t['completed'] else "No"
            ]
            task_list_to_write.append(";".join(str_attrs))
        task_file.write("\n".join(task_list_to_write))
    print(Colors.GREEN + "Task successfully added." + Colors.RESET)

    # Updates the tasks file with the modified task list
    update_task_in_file(task_list, new_task)


# Creates function to initialize task_list
def read_tasks_from_file(file_path):
    task_list = []  # Initializes an empty list to store task dictionaries

    try:
        with open(file_path, 'r') as task_file: 
            # Reads the content of the file and split it by newline character
            task_data = task_file.read().split("\n")
            # Removes empty strings from the list
            task_data = [t for t in task_data if t != ""]

        # Iterates over each task string in the task_data list
        for t_str in task_data:
            curr_t = {}  # Initializes an empty dictionary for the current task
            task_components = t_str.split(";")

            # Assigns values to keys in the curr_t dictionary based on 
            # task components
            curr_t['username'] = task_components[0]
            curr_t['title'] = task_components[1]
            curr_t['description'] = task_components[2]
            # Converts the due date string to datetime object 
            # using specified format
            curr_t['due_date'] = datetime.strptime(task_components[3],
            DATETIME_STRING_FORMAT)
            # Converts the assigned date string to datetime object 
            # using specified format
            curr_t['assigned_date'] = datetime.strptime(task_components[4], 
            DATETIME_STRING_FORMAT)
            # Sets the 'completed' key based on the string value 
            #('Yes' or 'No')
            curr_t['completed'] = True if task_components[5] == "Yes" else False
            # Appends the current task dictionary to task_list
            task_list.append(curr_t)
    
    # If tasks.txt does not exist, prints a message 
    # and initializes task_list as an empty list.
    except FileNotFoundError:
        print(Colors.RED 
        + "Tasks file not found. Initializing with empty task list." 
        + Colors.RESET)
        task_list = []

    return task_list


# Creates function to change the color of dates
def color_due_date(date, today):
    """
    Changes the color of a date based on its relation to today's date.

    Args:
        date (datetime.date): The date to be colored.
        today (datetime.date): Today's date.
        RED - overdue
        YELLOW - last day to complete
        GREEN - means you have at least two days to complete

    Returns:
        str: A formatted string representing the date with color codes.
    """
    
    if date < today:
        return f"{Fore.RED}{date.strftime(DATETIME_STRING_FORMAT)}{Style.RESET_ALL}"
    elif date == today:
        return f"{Fore.YELLOW}{date.strftime(DATETIME_STRING_FORMAT)}{Style.RESET_ALL}"
    else:
        return f"{Fore.GREEN}{date.strftime(DATETIME_STRING_FORMAT)}{Style.RESET_ALL}"


# Creates function to view all tasks
def view_all(task_list):
    # Loop through each task in the task list
    for i, t in enumerate(task_list, start=1):
        # Gets today's date
        today = datetime.today().date()

        # Initializes a string to display task information
        disp_str = Fore.GREEN + f"Task # {i}:\n" + Style.RESET_ALL

        disp_str += f"Task: \t\t {t['title']}\n"

        disp_str += (
        f"Assigned to: \t {Fore.MAGENTA}{t['username']}{Style.RESET_ALL}\n")

        disp_str += f"Date Assigned: \t {t['assigned_date'].strftime(
        DATETIME_STRING_FORMAT)}\n"

        disp_str += (
        f"Due Date: \t {color_due_date(t['due_date'].date(), today)}\n")

        disp_str += f"Task Description: \n {t['description']}\n"
        
        # Task completion status (colored RED uncompleted, GREEN completed)
        disp_str += (f"Completed: {Fore.GREEN}Yes{Style.RESET_ALL}\n"
                    if t['completed'] else 
                    f"Completed: {Fore.CYAN}No{Style.RESET_ALL}\n")
        
        # Checks if the user assigned to the task has been deleted
        if t['username'] not in username_password:  # Check if user is deleted
            disp_str += f"{Fore.RED}User deleted{Style.RESET_ALL}\n"
        # Prints the formatted task information
        print(disp_str)

    # Calls function to choose task to edit
    selected_task = choose_task_to_edit(task_list)
    
    if selected_task is None:
        return


# Creates function to view user's tasks
def view_mine(task_list, curr_user):
    # Flag to track if tasks are found for the current user
    tasks_found = False

    while True:
        # Loop through each task in the task list
        for i, t in enumerate(task_list, start=1):
            # Checks if the task is assigned to the current user
            if t['username'] == curr_user:
                tasks_found = True  # Set tasks_found to True
                today = datetime.today().date()
                # Constructs the display strings for the task
                disp_str = f"{Fore.LIGHTBLUE_EX}Task #{i}{Style.RESET_ALL}:\n"
                disp_str += f"Title: {t['title']}\n"
                disp_str += f"Assigned to: {t['username']}\n"
                disp_str += f"Date Assigned: {t['assigned_date'].strftime(
                DATETIME_STRING_FORMAT)}\n"
                
                # Colors and displays the due date based on its 
                # relation to today's date
                disp_str += (
                f"Due Date: {color_due_date(t['due_date'].date(), today)}\n")

                disp_str += f"Task Description: {t['description']}\n"

                # Indicate if the task is completed or not
                disp_str += (
                f"Completed: {Colors.GREEN + 'Yes'
                + Colors.RESET if t['completed'] else Colors.RED + 'No' 
                + Colors.RESET}\n"
                )

                print(disp_str)

        # Check if tasks are found for the current user
        if not tasks_found:
            print()
            print(Colors.RED + "You have no tasks" + Colors.RESET)
            break  # Exit the loop if no tasks are found
        
        # Calls function to choose a task to edit
        selected_task = choose_task_to_edit(task_list)

        # Exit the loop if the user chooses not to edit task
        if selected_task is None:
            break
    

''' I have create the function below to enhance possibility edit 
tasks from both menus 'view mine' and 'view all'
'''
def choose_task_to_edit(task_list):
    while True:
        # Prompt the user to select a task for editing or 
        # return to the main menu
        try:
            task_number = int(input(
            Colors.YELLOW + "Enter the number of the task you want to edit, or" 
            + Colors.RESET + Colors.BLUE + " 0 " + Colors.RESET 
            + Colors.YELLOW + "for main menu: " + Colors.RESET
        ))
           
        except ValueError:
            print(Colors.RED + "Invalid input." + Colors.RESET)
            print()
            continue
                    
        if task_number == 0:
            # Break out of the loop and return to the main menu
            return 

        # Checks if the task number exists 
        if task_number < 1 or task_number > len(task_list):
            print(Colors.RED + "Invalid task number." + Colors.RESET)
            print()
            continue

        selected_task = task_list[task_number - 1]  # Adjust for 0-based index

        # Checks if task completed, continue with menu
        if selected_task['completed']:
            print(Colors.RED + "Sorry, you can't edit completed tasks" 
            + Colors.RESET)
            print()
            continue
        
        # Checks if the selected task is overdue
        if selected_task['due_date'].date() < datetime.today().date():
            print(Colors.RED + "Sorry, you can't edit overdue tasks." 
            + Colors.RESET)
            print() 
            continue
        
        # Prompts user to edit task yes or no 
        edit_option = input(Colors.YELLOW 
        + "Do you want to edit this task? (y/n): " 
        + Colors.RESET).lower()

        # Executes program to edit task 
        if edit_option == 'y':
            if edit_task(selected_task, task_list):
                update_task_in_file(task_list, selected_task)
                break
        
        # If user chooses not to edit task, informs them and 
        # comes back to the menu 
        elif edit_option == 'n':
            print(Colors.RED + "Task will not be edited." + Colors.RESET)
            print()

        else:
            print(Colors.RED + "Invalid option." + Colors.RESET)
            print()

    return selected_task


# Creates function to edit tasks
def edit_task(task, task_list):

    # Checks if the task is already completed
    if task['completed']:
        print(Colors.RED 
        + "This task is already completed. You cannot modify it." 
        + Colors.RESET)
        print()
        return

    # Prompts user to choose an action
    while True:
        print(Colors.CYAN + "Choose an action:" + Colors.RESET)
        print("1. Mark as completed")
        print("2. Modify username")
        print("3. Modify due date")
        print("-1. Return to choose the task for modify")
        
        action_choice = input(Colors.YELLOW 
        + "Enter the number corresponding to " \
        "your choice: " + Colors.RESET)

        # Marks as completed
        if action_choice == '1':
            task['completed'] = True
            print(Colors.GREEN + "Task updated successfully."
                  + Colors.RESET)
            
            # Update the task list in the file
            update_task_in_file(task_list, task)

            break

        # Modifies the username of the task
        elif action_choice == '2':
            new_username = input(Colors.YELLOW + "Enter the new username: " 
            + Colors.RESET)
            # Checks if user exist
            if new_username not in username_password.keys():
                print(Colors.RED 
                + "User does not exist. Please enter a valid username" 
                + Colors.RESET)
                print()
                return
            
            task['username'] = new_username

            print()
            print(Colors.GREEN + "Task modified successfully"
                  + Colors.RESET)

            # Updates the task list in the file
            update_task_in_file(task_list, task)
            break

         # Modifies the due date of the task 
        elif action_choice == '3':
            while True:
                try:
                    # Prompts user for the due date update
                    task_due_date = input(Colors.YELLOW 
                    + "Due date of task (DD-MM-YYYY): " 
                    + Colors.RESET)

                    # Parses the user's input as a datetime object using 
                    # the specified format
                    due_date_time = datetime.strptime(
                    task_due_date, DATETIME_STRING_FORMAT)

                    # Checks if the new due date is in the past
                    if due_date_time.date() < date.today():
                        print(Colors.RED 
                        + "Sorry, you can't edit task to overdue"
                        + Colors.RESET)

                        # Continues the loop to prompt user for a valid due date
                        continue

                    break  # Exit the loop if the due date is valid
                
                except ValueError:
                    print(Colors.RED + "Invalid datetime format. Please use" \
                    "the format specified" + Colors.RESET)
                    print()

            # Updates due date        
            task['due_date'] =  due_date_time

            # Updates the task list in file
            update_task_in_file(task_list, task)
            print(Colors.GREEN + "Task updated successfully." + Colors.RESET)
            print()
            break 

        # Returns to the main menu
        elif action_choice == '-1':
            return

        else:
            print(Colors.RED + "Invalid choice. No changes made." 
            + Colors.RESET)

            print()
            continue


# Creates function to delete tasks by admin
def delete_task_by_number(task_list, task_number, curr_user):
        
    # Checks if the task number is valid
    if task_number < 1 or task_number > len(task_list):
        print(Colors.RED + "Invalid task number" + Colors.RESET)
        return False  

    # Prompts user to confirm deletion of the task
    delete_task_option = input(Colors.YELLOW 
    + "Do you want to delete this task (y/n)?"
    + Colors.RESET)

    if delete_task_option == 'y':
        # Delete the task from the task list
        del task_list[task_number - 1]
        return True
    else:
        return


# Creates function to update tasks in the tasks.txt file
def update_task_in_file(task_list, task):
    with open("tasks.txt", "w") as task_file:
        # Initializes an empty list to store task data in string format
        task_list_to_write = []
        # Iterates over each task in the task_list
        for t in task_list:
            # Converts task attributes to strings and appends to a list
            str_attributes = [
                t['username'],
                t['title'],
                t['description'],
                t['due_date'].strftime(DATETIME_STRING_FORMAT),
                t['assigned_date'].strftime(DATETIME_STRING_FORMAT),
                "Yes" if t['completed'] else "No"
            ]

            # Joins the task attributes with ';' and 
            # appends to the task_list_to_write
            task_list_to_write.append(";".join(str_attributes))

        # Writes the task data to the tasks.txt file, each task on a new line
        task_file.write("\n".join(task_list_to_write))


# Creates function to generate and write task overview to task_overview.txt
def generate_task_overview(task_list):
    today = datetime.today()

    # Calculates total number of tasks
    total_tasks = len(task_list)

    # Calculates total number of completed tasks
    completed_tasks = sum(task['completed'] for task in task_list)

    # Calculate total number of uncompleted tasks
    uncompleted_tasks = total_tasks - completed_tasks

    # Calculate total number of overdue tasks
    overdue_tasks = sum(1 for task in task_list
    if not task['completed'] and task['due_date'].date() < today.date())

    # Calculate percentage of incomplete tasks
    percentage_incomplete = (uncompleted_tasks / total_tasks) * 100 \
        if total_tasks > 0 else 0

    # Calculate percentage of overdue tasks
    percentage_overdue = (overdue_tasks / total_tasks) * 100 \
        if total_tasks > 0 else 0

    # Write task overview to task_overview.txt
    with open("task_overview.txt", "w") as task_overview_file:
        task_overview_file.write("Task Overview\n\n")

        task_overview_file.write(f"Total number of tasks: {total_tasks}\n")

        task_overview_file.write(f"Total number of completed tasks: "
                                 f"{completed_tasks}\n")

        task_overview_file.write(f"Total number of uncompleted tasks: "
                                 f"{uncompleted_tasks}\n")

        task_overview_file.write(
            f"Total number of tasks not completed and due to overdue: "
        f"{overdue_tasks}\n")

        task_overview_file.write(f"% of tasks that are incomplete:"
        f"{percentage_incomplete:.2f}%\n")

        task_overview_file.write(f"% of tasks that are overdue: "
        f"{percentage_overdue:.2f}%\n\n")

        # Write details of each task to the file
        for index, task in enumerate(task_list, start=1):

            task_overview_file.write(f"Task {index}:\n")

            task_overview_file.write(f"Title: {task['title']}\n")

            task_overview_file.write(f"Assigned to: {task['username']}\n")

            task_overview_file.write(f"Due Date: "
            f"{task['due_date'].strftime(DATETIME_STRING_FORMAT)}\n")

            task_overview_file.write(f"Description: {task['description']}\n")

            # Write task status (completed or not completed)
            status = 'Completed' if task['completed'] else 'Not Completed'
            task_overview_file.write(f"Status: {status}\n")

            # Check if the user assigned to the task deleted
            if task['username'] not in username_password:  
                task_overview_file.write("User deleted\n")

            task_overview_file.write("\n")


# Creates function to display statistics by admin only
def display_statistics(curr_user, username_password):
    
    # Checks if tasks.txt and user.txt exist, generate them if not
    if not os.path.exists("tasks.txt") or not os.path.exists("user.txt"):
        print(Colors.PURPLE + "Generating necessary files..." + Colors.RESET)

        # Creates an empty tasks.txt file
        with open("tasks.txt", "w") as task_file:
            pass  
        
        # Creates a user.txt file with admin credentials
        with open("user.txt", "w") as user_file:
            user_file.write("admin;password")  

    # Read tasks from tasks.txt file
    task_list = read_tasks_from_file("tasks.txt")

    # Read user data from user.txt file
    username_password = read_user_data()

    # Calculates statistics
    total_tasks = len(task_list)

    # Calculates completed tasks
    completed_tasks = sum(task['completed'] for task in task_list)

    # Calculates uncompleted tasks
    uncompleted_tasks = total_tasks - completed_tasks
    
    # Calculates overdue tasks
    overdue_tasks = sum(1 for task in task_list
    if not task['completed'] and task['due_date'].date() \
          < datetime.today().date())

    # Calculates % uncompleted tasks
    percentage_incomplete = (uncompleted_tasks / total_tasks) * 100 \
        if total_tasks > 0 else 0
    
    # Calculates % overdue tasks
    percentage_overdue = (overdue_tasks / total_tasks) * 100 \
        if total_tasks > 0 else 0

    # Displays statistics
    print(Colors.GREEN + "Statistics displayed successfully." + Colors.RESET)
    print()
    print(Colors.PURPLE + "\nStatistics:" + Colors.RESET)

    print(f"Total number of tasks: {total_tasks}")

    print(f"{Fore.GREEN}Total number of completed tasks: "
    f"{Style.RESET_ALL} {completed_tasks}")

    print(f"{Fore.CYAN}Total number of uncompleted tasks: "
    f"{Style.RESET_ALL} {uncompleted_tasks}")

    print(f"{Fore.RED}Total number of tasks not completed and due to overdue: "
    f"{Style.RESET_ALL}" 
    f"{overdue_tasks}")

    print(f"{Fore.CYAN}% of tasks that are incomplete: "
    f"{Style.RESET_ALL} {percentage_incomplete:.2f}%")

    print(f"{Fore.RED}% of tasks that are overdue: "
    f"{Style.RESET_ALL} {percentage_overdue:.2f}%\n")


# Creates function to generate and write user overview to user_overview.txt
def generate_user_overview(username_password, task_list):
    total_users = len(username_password)
    total_tasks = len(task_list)
    
    # Checks if there are no users or tasks available
    if total_users == 0 or total_tasks == 0:
        print("No users or tasks available.")
        return
    # Opens user_overview.txt file for writing
    with open("user_overview.txt", "w") as user_overview_file:
        # Writes to the file
        user_overview_file.write("User Overview\n\n")
        user_overview_file.write(f"Total number of users: {total_users}\n")
        user_overview_file.write(f"Total number of tasks: {total_tasks}\n\n")

        # Iterates over each user to calculate and write their task statistics
        for username, password in username_password.items():
            # Filter tasks assigned to the current user
            user_tasks = [
            task for task in task_list if task['username'] == username
            ]

            # Calculates total user's tasks
            total_user_tasks = len(user_tasks)

            # Calculates sum completed tasks by user
            completed_user_tasks = sum(task['completed'] for task in user_tasks)

            # Calculates sum of overdue user's tasks
            overdue_user_tasks = sum(
            1 for task in user_tasks
            if not task['completed'] \
            and task['due_date'].date() < datetime.today().date())

            # Calculates incomplete user's tasks
            incomplete_user_tasks = total_user_tasks - completed_user_tasks

            # Calculates percentage statistics:
            # Calculates % user's task in total tasks
            percentage_total_user_tasks = (total_user_tasks / total_tasks) * 100 \
            if total_tasks > 0 else 0

            # Calculates % completed user's tasks
            percentage_completed_user_tasks = (
            completed_user_tasks / total_user_tasks
            ) * 100 if total_user_tasks > 0 else 0

            # Calculates % must be completed
            percentage_must_completed = (
            incomplete_user_tasks / total_user_tasks
            ) * 100 if total_user_tasks > 0 else 0

            # Calculates % overdue user's tasks
            percentage_overdue_user_tasks = (
            overdue_user_tasks / total_user_tasks
            ) * 100 if total_user_tasks > 0 else 0

            # Write user-specific statistics to the file:
            # User's name
            user_overview_file.write(f"User: {username}\n")

            # Total number of tasks assigned to the user
            user_overview_file.write(f"Total number of tasks assigned: "
            f"{total_user_tasks}\n")

            # % of total tasks assigned to the user 
            user_overview_file.write(
            f"% of total tasks assigned: {percentage_total_user_tasks:.2f}%\n")

            # % of assigned and completed
            user_overview_file.write(
            f"% of tasks assigned and completed: " 
            f"{percentage_completed_user_tasks:.2f}%\n")

            # % must be completed
            user_overview_file.write(
            f"% of tasks must be completed: {percentage_must_completed:.2f}%\n")

            # % not completed and overdue
            user_overview_file.write(
            f"% of tasks not yet completed and are overdue: "
            f"{percentage_overdue_user_tasks:.2f}%\n")
            user_overview_file.write("\n")


# Creates function for checks if current user is admin
def admin_check(curr_user):
    # Checks if the current user is admin & enhance admin's rights
    if curr_user != 'admin':
        print(Colors.RED + "This option available for the admin only" 
        + Colors.RESET)
        return False
    else:
        return True


# Calls function to read user data
username_password = read_user_data()

# Calls function for login
curr_user = login(username_password)

# Calls function to read tasks data
task_list = read_tasks_from_file("tasks.txt")

# This block of code 'Main menu' executes the program 
while True:
    print()
    menu = input(
    f'''{Fore.YELLOW}Select one of the following Options below: {Style.RESET_ALL} 
    r - Registering a user
    d - Delete a user (admin only)                 
    a - Adding a task
    del - Delete task (admin only)
    va - View all tasks
    vm - View my task
    ds - Display statistics (admin only)
    gr - Generate reports (admin only)
    e - Exit
    : ''').lower()

    # In the block below calls functions depends on 
    # user's choice; errors handling
    if menu == 'r':
        register_user(username_password)

    elif menu == 'd':        
        if admin_check(curr_user):  # Checks if current user is admin  
            delete_user(username_password, task_list)
        
        else:
            continue  # Go back to main menu

    elif menu == 'a':
        add_task(task_list, username_password)

    elif menu == 'del':        
        if admin_check(curr_user):  # Checks if current user is admin
            try:
                task_number_to_delete = int(input(Colors.YELLOW + 
                "Enter the number of the task you want to delete: " 
                + Colors.RESET))
            except ValueError:
                print(Colors.RED + "Invalid input. Please enter a number." 
                + Colors.RESET)
                continue # Go back to the main menu 

            if delete_task_by_number(task_list, task_number_to_delete, curr_user):
                print(Colors.GREEN + "Task deleted successfully." + Colors.RESET)
                update_task_in_file(task_list, curr_user)  
            else:
                print(Colors.RED + "Failed to delete task." + Colors.RESET)
                continue  # Go back to the main menu

        else:
            continue  # Go back to main menu

    elif menu == 'va':
        view_all(task_list)

    elif menu == 'vm':
        view_mine(task_list, curr_user)
    
    elif menu == 'ds':
        if admin_check(curr_user):  # Checks if current user is admin
            display_statistics(curr_user, username_password)
        else:
            continue  # Go back to main menu        

    elif menu == 'gr':
        if admin_check(curr_user):  # Checks if current user is admin
            generate_task_overview(task_list)
            generate_user_overview(username_password, task_list)
            print(Colors.GREEN + "Reports generated successfully." 
            + Colors.RESET)

        else:
            continue  # Go back to main menu
            
    elif menu == 'e':
        print(Colors.PURPLE + 'Goodbye!!!' + Colors.RESET)
        exit()

    else:
        print(Colors.RED + "You have made a wrong choice. Please try again" 
        + Colors.RESET)
