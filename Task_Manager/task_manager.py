from datetime import datetime, date
from colorama import Style, Back, Fore, init
from tabulate import tabulate

# All statements are displayed in red, all inputs in white.
init(autoreset=True)


def get_user_match_status(user_input, user_list):
    """
    Check user input for task assignment.
    This allows the user to enter the user number or name.
    Returns 0 for false, 1 for integer input, 2 for string input.
    """
    user_type = 0
    user_input = user_input.strip().lower()

    try:
        user_input_int = int(user_input)
        if user_input_int in user_list:
            user_type = 1

    except ValueError:
        for key, value in user_list.items():
            if user_input == value[0].lower():
                user_type = 2
                break

    return user_type


def resolve_username(input_type, user_input, user_list):
    """
    Function to print the selected username for confirmation
    input_type is 1 if user input was a number and 2 if a string
    """
    if input_type == 1:
        user_input = int(user_input)
        return user_list[user_input][0].strip()
    else:
        return user_input.strip().lower()


def resolve_user_number(username_input, user_list):
    """Return the user number (key) given a username."""

    for key, value in user_list.items():
        try:
            if value[0].lower() == username_input.lower():
                return key
        except AttributeError:
                return int(username_input)


def normalize_date_format(unformatted_date):
    """
    Check if year is 4 digits, and month and day are 2.
    If not add zeros as required.
    The same decade is assumed for year, unless 0 is entered.
    """
    from datetime import date
    year = str(date.today().year)
    next_decade = str(int(year) + 10)

    while len(unformatted_date) != 10:
        if unformatted_date[0] == "0":
            unformatted_date = next_decade[0:3] + unformatted_date
        if unformatted_date[1] == "-":
            unformatted_date = year[0:3] + unformatted_date
        if unformatted_date[2] == "-":
            unformatted_date = year[0:2] + unformatted_date
        if unformatted_date[6] == "-":
            unformatted_date = unformatted_date[0:5] + "0" + unformatted_date[5:]
        if len(unformatted_date) == 9:
            unformatted_date = unformatted_date[0:8] + "0" + unformatted_date[-1]
    return unformatted_date


def format_output2_display(tasks, selected_user=False, user=None):
    """
    Output 2 as specified in the task
    Output each task as a block of data.
    Separate each block with line spaces
    """

    for row in tasks:
        print(f"""
    {Fore.RED}{"_" * 40}
    Task:                {row[1].strip()}
    Assigned to:         {row[0].strip().title()}
    Date assigned:       {row[4].strip()}
    Due Date:            {row[3].strip()}
    Task Complete?       {row[5].strip()}
    Task description:
     {row[2].strip()}
    {"_" * 40}"""
        )


def print_task_table(tasks, selected_user=False, user=None):
    """
    Use of tabulate to print tasks.
    Assigns task numbers to all tasks.
    Can print only tasks assigned to the user as required.
    User is capitalised for display only.
    """

    headers = [
        "TASK NUMBER",
        "USER",
        "TITLE",
        "DESCRIPTION",
        "DUE DATE",
        "DATE ENTERED",
        "DONE"
    ]

    processed_tasks = []
    task_number = 1

    for row in tasks:

        if len(row) == 6:
            if(
                not selected_user
                or row[0].strip().lower() == user.strip().lower()
            ):
                display_user = row[0].title()
                processed_tasks.append([task_number, display_user] + row[1:])
        else:
            print(f"Data in task {task_number} is corrupted.")

        task_number += 1

    table = tabulate(
        processed_tasks,
        headers=headers,
        tablefmt='grid',
        stralign='center',
        numalign='center',
    )

    print(f"{Fore.RED}{table}")


def print_user_tasks(tasks, user, selected_user=True):
    """
    Use of tabulate to print tasks.
    Assign task number to tasks.
    Print only tasks assigned to active user.
    Only displays non-complete task.
    User is capitalised for display only.
    """

    headers = [
        "TASK NUMBER",
        "USER",
        "TITLE",
        "DESCRIPTION",
        "DUE DATE",
        "DATE ENTERED",
        "DONE"
    ]

    processed_tasks = []
    task_number = 1

    for row in tasks:

        if len(row) == 6:
            if(
                row[0].strip().lower() == user.strip().lower()
                and row[5].strip().lower() == "no"
            ):
                display_user = row[0].title()
                processed_tasks.append([task_number, display_user] + row[1:])

        else:
            print(f"Data in task {task_number} is corrupted.")

        task_number += 1

    table = tabulate(
        processed_tasks,
        headers=headers,
        tablefmt="grid",
        stralign="center",
        numalign="center",
    )

    print(f"{Fore.RED}{table}")


def legacy_print_task_table(tasks, selected_user=False, user=None):
    """
    Legacy approach for printing the task table.
    No longer in use (kept for reference.)
    Alternative output option.
    Nicely prints all tasks with evenly spaced columns.
    Runs through every column (headers and tasks) to find max width.
    Sets all columns to max width and centers values.
    """

    headers = [
            "TASK NUMBER",
            "USER",
            "TITLE",
            "DESCRIPTION",
            "DUE DATE",
            "DATE ENTERED",
            "DONE"
    ]

    max_length = max(len(item) for item in headers)

    for row in tasks:
        for col in row:
            length = len(col)
            if length > max_length:
                max_length = length

    separator = ["-" * max_length] * len(headers)

    print(f"{Fore.RED}\n")
    print(" | ".join(item.center(max_length) for item in headers))
    print(" | ".join(separator))

    task_number = 1

    if not selected_user:
        for row in tasks:
            row_task_number = [str(task_number)] + row
            print(
                " | ".join(col.strip().title().center(max_length)
                for col in row_task_number)
            )
            task_number += 1
    else:
        for row in tasks:
            if row[0] == user:
                row_task_number = [str(task_number)] + row
                print(
                    " | ".join(col.strip().title().center(max_length)
                    for col in row_task_number)
                )
            task_number += 1

    print(f"\n")


def legacy_print_user_tasks(tasks, user, selected_user=True):
    """
    Legacy approach for printing the task todo table.
    No longer in use (kept for reference.)
    Nicely prints one task with evenly spaced columns.
    Runs through every column (headers and tasks) to find max width.
    Sets all columns to max width and centers values.
    Ignores tasks marked as complete.
    """

    user = user.strip().lower()

    headers = [
        "TASK NUMBER",
        "USER",
        "TITLE",
        "DESCRIPTION",
        "DUE DATE",
        "DATE ENTERED",
        "DONE"
    ]

    max_length = max(len(item) for item in headers)

    for row in tasks:
        for col in row:
            length = len(col)
            if length > max_length:
                max_length = length

    separator = ["-" * max_length] * len(headers)

    print(f"{Fore.RED}\n")
    print(" | ".join(item.center(max_length) for item in headers))
    print(" | ".join(separator))

    task_number = 1

    for row in tasks:
        if row[0].strip().lower() == user.strip().lower() and row[5].strip().lower() == "no":
            row_task_number = [str(task_number)] + row
            print(
                " | ".join(col.strip().title().center(max_length)
                for col in row_task_number)
            )
        task_number += 1

    print(f"\n")


def get_date_input():
    """
    Checks all year, month and day inputs are valid.
    Day input depends on entered month.
    """
    while True:
        try:
            year = int(input("Year: "))
            if year < 0 or 100 <= year <= 999 or year > 9999:
                    print(
                        f"{Fore.RED}"
                        "\nPlease enter the year (e.g. 7, 27, or 2027).\n"
                        "You can use 1, 2, or 4 digits — 3-digit years like "
                        "'125' are not allowed.\n"
                        f"{Style.RESET_ALL}"
                    )
            else:
                 break
        except ValueError:
            print(
                f"{Fore.RED}"
                "\nPlease enter the year (e.g. 7, 27, or 2027).\n"
                "You can use 1, 2, or 4 digits — 3-digit years like "
                "'125' are not allowed.\n"
                f"{Style.RESET_ALL}"
            )

    today_year = str(date.today().year)
    # Returns decade (e.g. 2020)
    today_year_3 = int(today_year[0:3]) * 10
    # Returns millennium (e.g. 2000)
    today_year_2 = int(today_year[0:2]) * 100

    if year < 10:
        entered_year = today_year_3 + year
    elif year < 100:
        entered_year = today_year_2 + year
    else:
        entered_year = year

    while True:
        try:
            month = int(input("Month: "))
            if not 1 <= int(month) <= 12:
                    print(
                        f"{Fore.RED}"
                        "\nPlease enter a month from 1 to 12.\n"
                        f"{Style.RESET_ALL}"
                        )
            else:
                 break
        except ValueError:
            print(
                f"{Fore.RED}"
                "\nPlease enter a month from 1 to 12.\n"
                f"{Style.RESET_ALL}"
                )

    while True:
            try:
                day = input("day: ")
                if int(month) == 2:
                    if 1 <= int(day) <= 28:
                        break
                    # Leap year can divide by 4
                    # If divisible by 100 must be divisible by 400
                    elif int(day) == 29:
                        if entered_year % 400 == 0:
                            break
                        elif(
                            entered_year % 100 != 0
                            and entered_year % 4 == 0
                        ):
                            break
                        else:
                            print(
                                f"{Fore.RED}"
                                "\nPlease enter a day from "
                                "1st to 28th February\n"
                            )
                    else:
                        print(
                            f"{Fore.RED}\nPlease enter a valid day\n"
                        )

                elif int(month) in (4, 6, 9, 11):
                    if not 1 <= int(day) <= 30:
                        print(
                            f"{Fore.RED}\nPlease enter "
                            "a day from 1st to 30th\n"
                        )
                    else:
                        break

                else:
                    if not 1 <= int(day) <= 31:
                        print(
                            f"{Fore.RED}\nPlease enter a day "
                            "from 1st to 31st\n"
                        )
                    else:
                        break
            except ValueError:
                print(
                    f"{Fore.RED}\n"
                      "Please enter a valid number.\n"
                      f"{Style.RESET_ALL}"
                )

    return f"{year}-{month}-{day}"


def modify_user_record(users_list, input_key, user_number=None, del_user=True, reassign=True):
    """
    Check if they require user to be deleted or not.
    Check if the user requires reassignment once deleted.
    """
    if del_user and not reassign:
        popped_user = users_list.pop(input_key)
        reassignment = False
    elif del_user:
        tasks = []
        old_username = users_list[input_key][0].strip().lower()
        new_username = users_list[user_number][0]
        reassignment = True

        with open("tasks.txt", "r") as f:
            for line in f:
                tasks_parts = line.strip().split(", ")
                if len(tasks_parts) == 6:
                    if  tasks_parts[0].strip().lower() == old_username:
                        tasks_parts[0] = new_username
                    tasks.append(tasks_parts)

        with open("tasks.txt", "w") as f:
            for task in tasks:
                f.write(", ".join(task) + "\n")

        popped_user = users_list.pop(input_key)

    else:
        popped_user = users_list[input_key][0]
        reassignment = False

    with open("user.txt", "w") as f:
        for key, value in users_list.items():
            f.write(f"{value[0]}, {value[1]}\n")
    if not reassignment:
        return popped_user, None
    else:
        return popped_user, tasks


def sync_task_list(edit_user=None, change=None, edit=False):
    """
    Reads from task file to create list.
    If edit is True, it will write changes.
    """
    tasks = []
    if edit_user and change:
        edit_user = edit_user.lower().strip()
        change = change.lower().strip()

    with open("tasks.txt", "r") as f:
        for line in f:
            tasks_parts = line.strip().split(", ")
            if len(tasks_parts) == 6:
                if edit:
                    if tasks_parts[0].strip().lower() == edit_user:
                        tasks_parts[0] = change
                tasks.append(tasks_parts)
    if edit:
        with open("tasks.txt", "w") as f:
            for task in tasks:
                f.write(", ".join(task) + "\n")

    return tasks


def edit_tasks(task_number, item_to_change, change_detail):
    """
    Reads from task file to create list.
    If edit is True, it will write changes.
    """
    tasks = []
    with open("tasks.txt", "r") as f:
        for index, line in enumerate(f):
            tasks_parts = line.strip().split(", ")
            if len(tasks_parts) == 6:
                if index == task_number - 1:
                    tasks_parts[item_to_change] = change_detail
                tasks.append(tasks_parts)

    with open("tasks.txt", "w") as f:
        for task in tasks:
            f.write(", ".join(task) + "\n")

    return tasks


# User list is retrieved from user.txt

users_credentials = {}
with open("user.txt", "r") as file:
    for index, line in enumerate(file):
        user_data_parts = line.strip().split(", ")
        username = user_data_parts[0]
        # Check if username already added and skips.
        if username.lower().strip() in [
            user[0].lower().strip() for user in users_credentials.values()
            ]:
            continue
        users_credentials[index] = (user_data_parts[0], user_data_parts[1])

today = date.today()
print("\nLogin\n")

# Print usernames for user selection.
for key, value in users_credentials.items():
    print(f"{Fore.RED}{key}. {value[0].title()}")

current_user = input("\nPlease enter the username or number: ")

# Checks the input (name or number) is valid.
user_match_status = get_user_match_status(current_user, users_credentials)

while  user_match_status == 0:
    current_user = input(
        "User not found. "
        "Please try again: "
    )
    user_match_status = get_user_match_status(current_user, users_credentials)

# Converts input to username.
current_user = resolve_username(
    user_match_status, current_user, users_credentials
).lower().strip()

print(f"{Fore.RED}\nUsername: {current_user.title()}")
user_number = resolve_user_number(current_user, users_credentials)

entered_password = input("\nPassword: ")

while users_credentials[user_number][1] != entered_password:
    entered_password = input(
        "\nPassword is incorrect.\n"
        "Please try again: ")

while True:
    # Present the menu to the user and
    # make sure that the user input is converted to lower case.
    menu_selection = input(
        f"{Fore.RED}\nSelect one of the following options:\n"
        "r  - register a user\n"
        "a  - add task\n"
        "va - view all tasks\n"
        "vm - view my tasks\n"
        "eu - edit users\n"
        "et - edit tasks\n"
        f"e  - exit\n"
        f"{Style.RESET_ALL}Selection: "
    ).lower()

    # Match active user to key 0 username in the list.
    # This ensure 1st user always has admin rights.
    if menu_selection == 'r' and current_user.lower() == users_credentials[0][0].lower():
        while True:
            new_user = input(
                "Please enter the new username: "
            ).strip().lower()
            while not 1 < len(new_user) < 10:
                print(
                    f"{Fore.RED}Please enter a username "
                    "between 2 and 10 characters.\n"
                    )
                new_user = input(
                    f"{Style.RESET_ALL}Please enter the new username: "
                ).strip().lower()
            user_exists = False

            for key, value in users_credentials.items():
                    if new_user == value[0].strip().lower():
                        user_exists = True  # Ensure no repeat users entered.

            while user_exists:
                entry_still_exists = False
                new_user = input(
                    f"{Fore.RED}\nUser already exists\n"
                    f"{Style.RESET_ALL}Please enter the new username: "
                ).strip().lower()
                for key, value in users_credentials.items():
                    if new_user == value[0].strip().lower():
                        entry_still_exists = True

                user_exists = entry_still_exists


            new_password = input("\nPlease enter the new password: ")
            confirm_password = input("\nPlease confirm your password: ")
            while new_password != confirm_password:
                new_password = input(
                    f"{Fore.RED}Your password did not match,{Style.RESET_ALL}"
                    "\nplease re-enter your password: "
                )
                confirm_password = input("Please confirm your password: ")

            with open("user.txt", "a") as file:
                file.write(f"\n{new_user}, {new_password}")

            add_another_user = input(
                "Do you want to add another user? "
                "(y or any other key to exit): "
            )

            if add_another_user != "y":
                break

    elif menu_selection == 'a':
        while True:
            for key, value in users_credentials.items():
                print(f"{Fore.RED}{key}. {value[0].title()}")
            assigned_user_input = input(
                "\nWhich user is required to complete the task. "
                "Please enter a number from the list, or type the name: "
            )
            # Function returns 0 for "user not found".
            assigned_user_status = get_user_match_status(assigned_user_input, users_credentials)
            while assigned_user_status == 0:
                assigned_user_input = input(
                    f"{Fore.RED}\nUser not found.\n"
                    "Which user is required to complete the task. "
                    "Please enter a number from the list, or type the name: "
                )
                assigned_user_status = get_user_match_status(assigned_user_input, users_credentials)

            # Function returns 1 for integer input and 2 for string input.
            if assigned_user_status == 1:
                assigned_user_input = int(assigned_user_input)
                print(
                    f"{Fore.RED}\nYou have selected "
                    f"{users_credentials[assigned_user_input][0].title()}")
            else:
                print(
                    f"{Fore.RED}You have selected "
                    f"{assigned_user_input.title()}"
                )

            assigned_user_input = resolve_username(
                assigned_user_status, assigned_user_input, users_credentials
            ).lower()

            task_title = input("Please enter the title of the task: ").title()
            task_description = input("Provide a brief description of the task: ")

            print(f"{Fore.RED}Please enter the year, month and day the task is due: ")

            input_date = get_date_input() # Gets date from user input
            # YYYY-MM-DD format.
            normalized_date = normalize_date_format(input_date)
            # Convert string to date object.
            input_date = datetime.strptime(normalized_date, "%Y-%m-%d").date()
            #Converts date to "DD Mon YYYY" format.
            written_date = input_date.strftime("%d %b %Y")
            today_written = today.strftime("%d %b %Y")

            # Re-enter date if in the past.
            while input_date < today:
                print(f"{Fore.RED}Please enter a date in the future.")

                input_date = get_date_input()
                normalized_date = normalize_date_format(input_date)

                input_date = datetime.strptime(
                    normalized_date, "%Y-%m-%d"
                ).date()

                written_date = input_date.strftime("%d %b %Y")

            task_complete_status = "No"

            # 2D list required for formatting_task_print
            new_task_entry = [
                [assigned_user_input,
                task_title,
                task_description,
                written_date,
                today_written,
                task_complete_status],
                ]

            # Print task to review.
            format_output2_display(new_task_entry)

            entry_confirmation = input(
                "\nEnter \"n\" to restart input. "
                "Enter \"e\" discard changes. Enter "
                "any other key to continue: "
            )
            # Restart "add task" section
            if entry_confirmation == "n":
                pass

            # Write task to file
            elif entry_confirmation != "e":
                with open("tasks.txt", "a") as file:
                    file.write(", ".join(new_task_entry[0]) + "\n")
                break

            # Skip writing task and move to end.
            else:
                break

    elif menu_selection == 'va':
        # Read and display all tasks.
        task_list = sync_task_list()
        print_task_table(task_list)

    elif menu_selection == 'vm':
        # Read tasks
        task_list = sync_task_list()

        task_filter_choice = input(
            "Select \"a\" to see all tasks or "
            "enter any other key to see "
            "only outstanding tasks: "
        )
        # Print all tasks for user including complete.
        if task_filter_choice == "a":
            print_task_table(
                task_list, selected_user = True, user = current_user
                )

        else:
            # Skip tasks marked as complete.
            print_user_tasks(task_list, current_user)

        while True:

            completed_task_input = input(
                "Please enter the task number you have completed. "
                "Press any other key to exit: "
            )

            try:
                completed_task_index = int(completed_task_input)

                # Check task exists
                if 1 <= completed_task_index <= len(task_list):

                    task_marked = False
                    with open("tasks.txt", "w") as file:
                        for index, task_entry in enumerate(task_list):
                            # Match index to input.
                            # Confirm task assigned to user.
                            if (
                                index == completed_task_index - 1
                            and task_entry[0].strip().lower() == current_user.strip().lower()
                            ):
                                task_entry[5] = "Yes"
                                task_marked = True
                                print(
                                    f"{Fore.RED}\nTask marked as complete."
                                    f""
                                )

                            file.write(", ".join(task_entry) + "\n")

                        if not task_marked:
                            print(
                                f"{Fore.RED}That task is not assigned to "
                                f"{current_user}"
                            )

                        # Print list according to user selection.
                        if task_filter_choice == "a":

                            print_task_table(
                                task_list, selected_user = True,
                                user = current_user
                            )

                        else:
                            print_user_tasks(
                                task_list, current_user
                            )

                else:

                    print(
                        f"{Fore.RED}That Task does not exist."
                        f""
                    )

            except ValueError:
                break

    elif menu_selection == 'eu' and current_user.lower() == users_credentials[0][0].lower():

        for key, value in users_credentials.items():
            if key == 0:
                pass
            else:
                print(
                    f"{Fore.RED}{key}. "
                    f"{value[0].title()}"
                )

        print(
            f"{Fore.RED}\nSelect user to edit or remove."
            f"\n"
        )
        selected_user_input = input("Select User: ")

        # Function returns 0 for "user not found".
        # Admin cannot be edited.
        selected_user_input_type = get_user_match_status(selected_user_input, users_credentials)
        while(
            selected_user_input_type == 0
            or selected_user_input == "0"
            or selected_user_input.lower().strip() == users_credentials[0][0].lower()
        ):
            user_match_status = 0
            selected_user_input = input(
                f"{Fore.RED}User not found.\n"
                f"Which user is to be edited "
                f"or removed.\n"
                "Please enter a number from the list, or type the name: "
            )
            selected_user_input_type = get_user_match_status(selected_user_input, users_credentials)

        # Function returns 1 for integer input and 2 for string input.
        if selected_user_input_type == 1:
            selected_user_input = int(selected_user_input)
            print(
                f"{Fore.RED}\nYou have selected "
                f"{users_credentials[selected_user_input][0].title()}")
        else:
            print(
                f"{Fore.RED}You have selected "
                f"{selected_user_input.title()}"
            )
        # Set input to username and retrieve key.
        selected_username = resolve_username(
            selected_user_input_type, selected_user_input, users_credentials
        ).lower()
        selected_user_number = resolve_user_number(selected_user_input, users_credentials)

        edit_type = input(
            "If you wish to delete user, select \"d\" "
            "else select \"e\" to edit. Enter any other"
            " key to exit: "
        )
        # Reprint user list minus the deleted user.
        if edit_type == "d":
            for key, value in users_credentials.items():
                if key == selected_user_number:
                    pass
                else:
                    print(
                        f"{Fore.RED}{key}. "
                        f"{value[0].title()}"
                    )

            print(
                f"{Fore.RED}\nSelect user to reassign tasks to."
                f"\n"
            )
            reassign_user_input = input("Select User: ")

            # Function returns 0 for "user not found".
            # Admin cannot be edited.
            reassign_user_input_type = get_user_match_status(reassign_user_input, users_credentials)
            while(
                reassign_user_input_type == 0
                or reassign_user_input == str(selected_user_number)
                or reassign_user_input.lower().strip() == users_credentials[selected_user_number][0].lower()
            ):
                reassign_user_found = 0
                reassign_user_input = input(
                    f"{Fore.RED}User not found.\n"
                    f"Which user is to be edited "
                    f"or removed.\n"
                    "Please enter a number from the list, or type the name: "
                )

            # Function returns 1 for integer input and 2 for string input.
            if reassign_user_input_type == 1:
                reassign_user_input = int(reassign_user_input)
                print(
                    f"{Fore.RED}\nYou have selected "
                    f"{users_credentials[reassign_user_input][0].title()}"
                    f""
                )
            else:
                print(
                    f"{Fore.RED}You have selected "
                    f"{reassign_user_input.title()}"
                )
            # Set input to username and retrieve key.
            reassign_username = resolve_username(
                reassign_user_input_type, reassign_user_input, users_credentials
            ).lower()
            reassign_user_number = resolve_user_number(reassign_username, users_credentials)
            deleted_user, task_list = modify_user_record(users_credentials, selected_user_number, reassign_user_number)

            print(
                f"\n{Fore.RED}{deleted_user[0].strip().title()} "
                f"has been deleted."
                )

        elif edit_type == "e":
            new_username = input(
                "Please enter the new username: "
            ).strip().lower()
            users_credentials[selected_user_number] = (new_username, users_credentials[selected_user_number][1])
            new_username, _ = modify_user_record(
                users_credentials,
                selected_user_number,
                del_user = False
                )
            task_list = sync_task_list(
                edit_user = selected_username,
                change = new_username,
                edit = True
                )
            print(
                f"\n{Fore.RED}{users_credentials[selected_user_number][0]}"
                f"has been changed to {new_username.title()}."
                f""
                )
        else:
            pass

    elif menu_selection == 'et' and current_user.lower() == users_credentials[0][0].lower():

        task_list = sync_task_list()
        print_task_table(task_list)

        while True:
            try:
                selected_input_task = int(
                    input("Please enter the task number to edit: ")
                )
                task_found = False
                # Check task exists and assigned to user.
                if 1 <= int(selected_input_task) <= len(task_list):

                    print(
                        f"{Fore.RED}"
                        "1. Title\n"
                        "2. Description\n"
                        "3. Due Date\n"
                        f""
                    )
                    while True:
                        try:
                            field_to_edit = int(
                                    input("To which option "
                                        "do you wish to edit? ")
                            )
                            #  Title, description or date due.
                            while not 1 <= field_to_edit <= 3:
                                print(
                                    f"{Fore.RED}\nInvalid input."
                                    "Please input an option of 1 to 3"
                                    f"\n"
                                )
                                field_to_edit = int(
                                    input("To which option "
                                    "do you wish to edit? ")
                                )

                            if field_to_edit == 1:
                                updated_value = input(
                                    "Please enter the "
                                    "title of the task: "
                                ).title()

                            elif field_to_edit == 2:
                                updated_value = input(
                                    "Provide a brief "
                                    "description of the task: "
                                )

                            else:
                                print(
                                    f"{Fore.RED}Please enter the "
                                    "year, month and day that the "
                                    f"task is due: "
                                    )

                                # Gets date from user input
                                input_date = get_date_input()
                                # YYYY-MM-DD format.
                                normalized_date = normalize_date_format(
                                    input_date
                                )
                                # Convert string to date object.
                                input_date = datetime.strptime(
                                    normalized_date, "%Y-%m-%d"
                                ).date()
                                #Converts date to "DD Mon YYYY" format.
                                updated_value = input_date.strftime(
                                    "%d %b %Y"
                                )
                                # Re-enter date if in the past.
                                while input_date < today:
                                    print(
                                        f"{Fore.RED}Please enter "
                                        "a date in the future."
                                        f""
                                        )

                                    input_date = get_date_input()
                                    normalized_date = normalize_date_format(
                                        input_date
                                    )
                                    input_date = datetime.strptime(
                                        normalized_date, "%Y-%m-%d"
                                    ).date()

                                updated_value = input_date.strftime(
                                    "%d %b %Y"
                                )

                            # read tasks.txt, add and writes changes.
                            task_list = edit_tasks(
                                selected_input_task,
                                field_to_edit,
                                updated_value
                                )

                            # confirm changes, print new list.
                            task_found = True
                            print_task_table(task_list)
                            break

                        except ValueError:
                            print(
                                f"{Fore.RED}\nInvalid input."
                                "Please input a option of 1, 2 or 3"
                                f"\n"
                            )
                if task_found:
                    break
                else:
                    print(
                        f"\n{Fore.RED}That task does not exist.\n"
                    )

            except ValueError:
                    print("Incorrect")

    elif menu_selection == "r" or menu_selection == "eu" or menu_selection == "et":
        # If "r" or "eu" selected by non-admin user.
        print(
            f"{Fore.RED}\nAdmin rights are required "
            f"to register new users.\n{Style.RESET_ALL}"
        )

    elif menu_selection == 'e':
            pass

    else:
            print(
                f"{Fore.RED}You have entered an invalid input. "
                f"Please try again"
            )

    # Once User has exited the menu selection.
    if menu_selection == "e":
        print(
        f"{Fore.RED}Changes have been saved.\n"
        f"Thank you and goodbye!"
        )
        break

    else:
        # Update user list for new registered users.
        users_credentials = {}
        with open("user.txt", "r") as file:
            for index, line in enumerate(file):
                user_data_parts = line.strip().split(", ")
                try:
                    username = user_data_parts[0]
                except IndexError:
                    continue
                # Check if username already added and skips.
                if username.lower().strip() in [
                    user[0].lower() for user in users_credentials.values()
                    ]:
                    continue
                try:
                    users_credentials[index] = user_data_parts[0], user_data_parts[1]
                except IndexError:
                    pass

        return_to_menu_choice = input(
            f"{Fore.RED}Do you wish to continue "
            f"back to the main menu?{Style.RESET_ALL}\n"
            "(press \"y\" to return, any key to exit): "
        ).lower().strip()
        if return_to_menu_choice != "y":
            print(
                f"{Fore.RED}Changes have been saved.\n"
                f"Thank you and goodbye!"
            )
            break
