# =========  Import Libraries  =========
# Import a date time library to help with getting the date when the task was set.
# Had to import datetime for task 26 to convert the date back to be able to compare it to see if it was overdue
# Reference for library and research is https://www.programiz.com/python-programming/datetime/current-datetime
import datetime
from datetime import date

# =========  Global Variables  =========
# Need these variables to check things in the main program and several functions.
user = ""
usernames = []
passwords = []

# =========  Define Functions  =========

def sort_user_pass():
    # This tells the function to use the global variables for username and password and store the data in the global variables
    global usernames
    global passwords
    # Open user text file to get all the information about the usernames and passwords
    f = open("user.txt", "r")
    user_content = ""

    # Getting all the content from user.txt a line at a time
    for line in f:
        user_content += line
    f.close()

    # Tidying the content to get rid of commas and split username and password into a list by each word
    user_content = user_content.replace(", ", " ")
    user_content = user_content.split()
    
    # Usernames are in the odd positions and passwords in the even positions in the user_content list. 
    # The list can be seperated into a username and password list by even and odd positions.
    # Each data point is in a comparible position in the password / username lists by using 'i'
    for i in range (0, len(user_content)):
        if   i % 2 == 0:
            usernames.append(user_content[i])
        else:
            passwords.append(user_content[i])

def login():
    # This tells the function to use the global variable 'user'so that in saves it and can call on it in different functions
    global user
    # Check to see if the user inputted username and passwords are in the lists and match.
    print("\nPlease enter your username and password to login.\n")
    while True:
        user = input("Enter your username: ")
        user = user.lower()
        pword = input("Enter your password: ")
        accept = False
        for i in range(len(usernames)):
            if usernames[i] == user and passwords[i] == pword:
                accept = True
                break
        if accept == True:
            print ("\nLogging in..... ")
            break
        # If the username matches but the password doesn't then it will give a different response
        elif user in usernames:
            print (f"\nPassword does not match the recognised username \'{user.capitalize()}\'. Please try again.")
            continue
        # If there is no match for the username then it will say it is not recognised. This tells the user that there is a mistake in both fields.
        else:
            print ("\nUsername and password not recognised. Please try again.")
            continue

def admin_menu():
    # Presenting a different menu_choice to 'admin' user. 
    # Making sure that the user input is converted to lower case.
    menu_choice = input(f'''Hello {user.capitalize()}. Please select one of the following options below:
r - Registering a User (admin only)
a - Adding a Task
va - View All Tasks
vm - View My Task
gr - Generate Reports (admin only)
ds - Display Statistics (admin only)
e - Exit
: ''').lower()
    return menu_choice

def normal_menu():
    # Menu for normal users (not admin) - return input as lowercase
    menu_choice = input(f'''Hello {user.capitalize()}. Please select one of the following options below:
r - Registering a User (Admin Only)
a - Adding a Task
va - View All Tasks
vm - View My Task
e - Exit
: ''').lower()
    return menu_choice

def reg_user():
# This will check to make sure user is admin, otherwise, it will go back to the main menu.
    if not user == "admin":
        print("\nOnly the admin user can register new users. Select another item from the main menu.\n")
    else:
        print("\nYou are admin and can register a new user.")
        while True:
            new_user = input("Please enter a new username: ")
            new_user = new_user.lower()
            # Will only accept a username of 2 or more characters
            if len(new_user) <= 1:
                print("You need to enter more than one character. Please try again")
                continue
            # Will not accept usernames with a 'space' in the text. This is to make sure data can be sorted correctly
            if new_user.find(" ") != -1 or new_user.find(",") != -1:
                print("You can not have a username with a space or a comma in, please try again: ")
                continue
            # If a username already exists it won't allow you to put another one in.
            if new_user in usernames:
                print("This username already exists, please try again")
                continue
            print("Username has been accepted!\n")
            while True:
                # Password must have more than five characters to make it secure (This wasn't in the task but thought it is a standardised required)
                new_pass = input(f"Please enter at least a six charatcer password for {new_user.capitalize()}: ")
                if len(new_pass) <= 6:
                    print("You need to enter more than six characters without commas or spaces. Please try again")
                    continue
                # Password cannot have a space in the string
                if new_pass.find(" ") != -1 or new_pass.find(",") != -1:
                    print("You can not have a password with a space or a comma in, please try again: ")
                    continue
                # A check to make sure the user has put the correct password in. If not it will start the password loop again until it is right.
                pass_check = input("Please enter the password again to check: ")
                if pass_check == new_pass:
                    print("Password has been accepted!\n")
                    break
                else:
                    print("Password did not match, please try again")
                    continue
            # Double check to see if they still wants to register a new user. Can't be undone. 
            add_user_check = input(f"Are you sure you want to register \'{new_user.capitalize()}\' as a user y/n: ")
            add_user_check = add_user_check.lower()
            if add_user_check == "y" or add_user_check == 'yes':
                f = open("user.txt", "a")
                f.write(f"\n{new_user}, {new_pass}")
                f.close()
                # Realised if you add a new user you need to update the username and password list.
                # Or, you can't assign them new tasks until you run a new session.
                usernames.append(new_user)
                passwords.append(new_pass)
                print(f"\n{new_user.capitalize()} has been added. Thank you.\n")
                break
            else:
                print(f"\n{new_user.capitalize()} has not been added to the register. Please try again if you want to add a new user\n")
                break

def add_task():
    # Any user can add a new task. Will step through several questions all with checks.
    print("\nYou can add a new task")
    while True:
        # Gives the user a chance to exit here as it is a long process if they want to proceed.
        task_user = input("Which user are you assigning the task to (or type \'e\' to exit): ")
        task_user = task_user.lower()
        if task_user == "e":
            break
        # Check to see if username exists before adding
        if task_user in usernames:
            print (f"User {task_user.capitalize()} added to task")
        else:
            print(f"User {task_user} does not exist, please try again")
            continue
        # Goes to task title fuction to return a string for the the task_title variable
        task_title = get_task_title()

        # Add decription to the task, again will check to see if something has been entered before continuing.
        task_description = get_task_description()

        
            # To get the due date in the right format described in the task, then the user will be led through some set questions.
            # These require exact responses to make sure the format is correct. However, this won't check if the numbers, months, years are a suitable answer.
            # This requires some responsibility from the user to try to put the right info in, and a date tha is suitable.
        task_due_date = get_task_due_date()
        
        # This uses the import datetime library module to get the current date without asking the user 
        # This inculdes putting it in the correct format.
        # Reference for research is # Reference for library and research is https://www.programiz.com/python-programming/datetime/current-datetime
        today = date.today()
        task_current_date = today.strftime("%d %b %Y")
        # It is assumed any task being added will not be completed as advised in the task, task complete set to 'No'
        task_complete = "No"
        # Final check to see if the task being entered is correct and in the right format as can't be undone.
        check_task = input(f"""Are you sure you want to add the task
_______________________________________________________________________________________________
Task:\t\t\t{task_title.capitalize()}
User:\t\t\t{task_user.capitalize()}
Date assigned:\t\t{task_current_date}
Due date:\t\t{task_due_date}
Task complete:\t\t{task_complete}
Task description:\t{task_description.capitalize()}
_______________________________________________________________________________________________

Do you want to add this task? y/n: """).lower()
        if check_task == 'y' or check_task == 'yes':
            # Task added to file
            f = open("tasks.txt", "a")
            f.write(f"\n{task_user}, {task_title}, {task_description}, {task_current_date}, {task_due_date}, {task_complete}")
            f.close()
            print("\nTask added to file task.txt. Thanks.\n")
            break
        else:
            # If 'no' task not added to file and will go back to the main menu.
            # If you want another go at adding a task you will need to start again from the main menu.
            print("\nTask not added to the file. Please try again if you want to add a new task\n")
            break
        break

# Gets the information for the task_tile variable and checks to see if teh string has characters
def get_task_title():
    # Add title, will check to make sure there are some characters entered
    while True: #loop until characteres have been added
        task_title = input("What is the title of the task: ")
        if task_title.find(",") != -1:
            print("You can't use comma\'s, please try again")
            continue
        if len(task_title) > 0:
            print("Task title has been added")
            break
        else:
            print("Nothing has been entered or you can't use comma\'s, please try again")
            continue
    return task_title

# Gets the information for the task description and checks to see if characters have been inputted
def get_task_description():
    while True: # loop until characters have been added
        task_description = input("What is the description of the task: ")
        if task_description.find(",") != -1:
            print("You can't use comma\'s, please try again")
            continue
        if len(task_description) > 0:
            print("Task description has been added")
            break
        else:
            print("Nothing has been entered or you can't use comma\'s, please try again")
            continue
        break
    return task_description

# Gets the due date information in a particular format and checks along the way that the information is set correctly as defined in the task
def get_task_due_date():
    while True: # loop until year is a 4 digit integer
        print ("What is the due date of the task:")
        year = input("Year (4 digits): ")
        try:
            if len(year) == 4:
                year = int(year)
                break
            else:
                print("This needs to be 4 digits long for example \'2022\'. Please try again")
        except:
            print("This needs to be 4 digits long for example \'2022\'. Please try again")
            continue
    
    while True: # loop to make sure month is the correct string of three characters long as set in the task.
        month = input("Month (3 first letters e.g. \'Apr\'): ").lower()
        try: # needed the month to be exactly this format or it wouldn't be the correct format or work when comparing later. 
            if month == 'jan' or month == 'feb' or month == 'mar' or month == 'apr' or month == 'may' or month == 'jun' or month == 'jul' or month == 'aug' or month == 'sep' or month == 'oct' or month == 'nov' or month == 'dec':
                break
            else:
                print("The month needs to be the first 3 characters of the month for example \'Sep\'. Please try again.")
        except:
            print("The month needs to be the first 3 characters of the month for example \'Sep\'. Please try again.")
            continue
    
    while True: # loop to make sure the date enetered is a on or two digit integer less than 31.
        day = input("Day (e.g. 05): ")
        try:
            if len(day) <= 2 and len(day) >= 1:
                day = int(day)
                if day <= 31 and day >= 1:
                    break
                else:
                    print("Please enter a date below 31.")
            else:
                print ("Day needs to be in number format with 2 or less digits e.g. \'15\' or \'03\'. Please try again.")
        except:
            print ("Day needs to be in number format with 2 or less digits e.g. \'15\' or \'03\'. Please try again.")
            continue
    
    # The day month year are put into the correct format to match the task.
    task_due_date = str(f"{day} {month.capitalize()} {year}")
    return task_due_date

def view_all():
    # This will show all the current tasks in the file for all users in the correct format.
    # It will open the files again as new information has been added and the data needs sorting into the correct format.
    print("\nThis will show all current tasks in the file\n")
    f = open ("tasks.txt", "r")
    task_num = 0
    # Use a for loop to get the information a line at a time from the file to show all tasks in a relevant easy to understand format.
    for line in f:
        task_num += 1
        print(f"TASK NUMBER: {task_num}")
        line = line.replace("\n", "")
        line = line.split(", ")
        print(f"""_______________________________________________________________________________________________
Task:\t\t\t{line[1].capitalize()}
User:\t\t\t{line[0].capitalize()}
Date assigned:\t\t{line[3]}
Due date:\t\t{line[4]}
Task complete:\t\t{line[5]}
Task description:\t{line[2].capitalize()}
_______________________________________________________________________________________________
        """)
    f.close()

def view_mine():
    edit_option = ""
# This will show all the tasks for the current user in the correct format.
# Again it will open the files as new info could have been entered and the data will need sorting.
# If the current user has no tasks it will state this.
    print("""\nThis will show all tasks for you in the file.
You can then selected the task number for more details (and edit the task if it is not completed)\n""")

    # Open the task.txt file to read the information for the specified user and transfer to the line variable in the simplified format for capstone 3.
    f = open ("tasks.txt", "r+")
    edited_file = ""
    task_num = 0
    
    for line in f:
        line = line.replace("\n", "")
        line = line.split(", ")
        if user == line[0]:
            task_num += 1
            print(f"{task_num}) Task: {line[1].capitalize()}   Due Date: {line[4]}   Complete: {line[5].capitalize()}")
    f.close()
    # loop to make sure the user can pick a task to edit with the correct number associated
    while True: # if the user has no tasks then it will let them know and exit the loop
        if task_num == 0:
            print (f"There are no tasks in the file for {user.capitalize()}. Please add some tasks to create work for {user.capitalize()}. Thanks.\n")
            break
        task_select = input("\nPlease select the number of the task, or \'-1\' to exit: ")
        try: # making sure the user has selected a number in the correct range
            task_select = int(task_select)
            if task_select == -1:
                break
            elif task_select > 0 and task_select <= task_num:
                break
            else:
                print (f"Please enter a whole number between 1 and {task_num} or \'-1\' to exit. Try again")
        except:
            print (f"Please enter a whole number between 1 and {task_num} or \'-1\' to exit. Try again")
    
    # this reads the information off the file and displays it a more detailed format (requested by capstone 3)
    f = open ("tasks.txt", "r+")
    task_num = 0
    for line in f:
        line = line.replace("\n", "")
        line = line.split(", ")
        if user == line[0]: # this is a process to makes sure the task_num is the same as the number the user selected. Counts how many times the username has come up and comares it to the selectiuon
            task_num += 1
            if task_num == task_select:
                print(f"Task Number: {task_num}") # print the correct task in the correct format.
                print(f"""_______________________________________________________________________________________________
Task:\t\t\t{line[1].capitalize()}
User:\t\t\t{line[0].capitalize()}
Date assigned:\t\t{line[3]}
Due date:\t\t{line[4]}
Task complete:\t\t{line[5]}
Task description:\t{line[2].capitalize()}
_______________________________________________________________________________________________
""")
                # this will now check to see if the task can be edited. if compleeted task is 'No' then it will allow the user to edit, otherwise it will say completed and go back to the main menu.
                if line[5] == "No":
                    while True: # loop to allow the user to edit the file in a number of ways - completed - user - due date
                        edit_option = input(menu_option())
                        if edit_option == '1': 
                            line[5] = "Yes"
                            print ("Task now marked as complete") # c
                        if edit_option == '2':
                            while True: # loop to change the user assigned and if they exist to allocate the task to them
                                task_user = input("Which user do you want to assign this task to: ")
                                task_user = task_user.lower()
                                # Check to see if username exists before adding
                                if task_user in usernames:
                                    print (f"User {task_user.capitalize()} added to task")
                                    line[0] = task_user
                                    break
                                else:
                                    print(f"User {task_user} does not exist, please try again")
                                    continue
                        if edit_option == '3':
                            # Use the function get task due date to get day, month, and year variables in the right format.
                            # Re used this function to make the code about 40 lines shorter - still works. 
                            task_due_date = get_task_due_date()
                            line[4] = task_due_date
                        if edit_option == '4':
                            print ("This will save any chamges made to the task")
                            # Task added to file all saves will happen outside the loop at the end and has currently saved the new edited information in teh edited_file variable
                            edited_file = (f"{edited_file}{line[0]}, {line[1]}, {line[2]}, {line[3]}, {line[4]}, {line[5]}\n")
                            print("\nTask added to file task.txt. Thanks.\n")
                            break
                        if edit_option == '5': # This will allow a user to exit without saving any of their changes and won't save the info to the edited_file variable
                            print("Nothing saved. The task below will not be saved and will be reverted to the original.... exiting to main menu")
                            break
                        print(f"Task Number: {task_num}")
                        print(f"""_______________________________________________________________________________________________
Task:\t\t\t{line[1].capitalize()}
User:\t\t\t{line[0].capitalize()}
Date assigned:\t\t{line[3]}
Due date:\t\t{line[4]}
Task complete:\t\t{line[5]}
Task description:\t{line[2].capitalize()}
_______________________________________________________________________________________________
""")
                else:
                    print("\nYou cannot edit this task as it is already completed\n")
    if edit_option == '4': # now if edited option '4' was selected (save chganges), it will run through the write to file process and change the task selected with the edited_file info
        #edited_file = (f"{edited_file}{line[0]}, {line[1]}, {line[2]}, {line[3]}, {line[4]}, {line[5]}")
        f = open("tasks.txt", "r")
        task_num = 0
        changer = 1 #  a variable to add the task number by one everytime the username matches so that it can select the right task that needs editing
        content = ""
        for line in f: # a for loop to get run therough the previous file information until it gets to the new edited part
            edit_line = line.replace("\n", "")
            edit_line = edit_line.split(", ")
            if user == edit_line[0]:
                task_num += changer # if the username matches it will add one onue onto task_number until the task_selected and task_number matches so that the correct task is chosen
            if task_num == task_select: # once task number and task selected matched it will copy in the new edited file info in the correct format and replace.
                content = (f"{content}{edited_file}")
                task_num = 0 #  this was to make sure task number wasn't equal to task select anymore
                changer = 0 # this was to make sure it wouildn't add one on everytime the selected user and task user matched so that i wouldn't trigger this in the loop again
            else:
                content = (f"{content}{line}") # if they don't match then just copy the original file into the content varaible and save the previous tasks
        f.close()
        f = open("tasks.txt", "w+")
        f.write(content) # once compelte open the file tasks.txt as writable and write over with the new formatted contnt and edited task
        f.close()
    elif line[4] == "Yes":
        print("You cannot edit a task that is already completed... Exiting to main menu") # if task selected is already completed, then don't edit

def menu_option(): # function to display the edit task option. Made this a function as the program might want to run this again at different times in the menu as it develops and builds on itself
    return ("""To edit this task select an option:
    1 - Mark as complete
    2 - Change the assigned user
    3 - Change the due date
    4 - Save all changes and exit
    5 - Do not save any changes / Exit to menu
    Choose a number between 1 - 5: """)

# this function will generate reports, I had to make it flexible as you generate reports both in the generate reports menu selection, but also the statistics selection
def generate_reports():
    # overview tasks  is a nested function as I wanted to run this code more than once in generated reports function, but it wasn't needed elsewhere in the code and didn't want to store the variables in the main memory
    def overview_tasks_text(): # this formats the task overview information to be displayed on screen and in the reports as neatly as possible for the user 
        return (f"""TASK OVERVIEW FOR ALL USERS

Number of tasks for all users = {count_tasks}

Number of tasks not completed = {count_tasks_not_completed}
    Percentage of tasks not completed = {((count_tasks_not_completed / count_tasks) * 100):.2f}%

Number of tasks completed = {count_tasks - count_tasks_not_completed}
    Percentage of tasks completed = {(((count_tasks - count_tasks_not_completed) / count_tasks) * 100):.2f}%

Number of taks overdue (all users) = {count_tasks_overdue}
    Percentage of tasks not completed and overdue = {((count_tasks_overdue / count_tasks) * 100):.2f}%
""")
    # overview of the users is a nested function as well. Again, I wanted to run this code more than once in generated reports function, but it wasn't needed elsewhere in the code and didn't want to store the variables in the main memory
    # It is a bot more complecated as you have to dispaly the information in the correct simple format for each user in the report and onscreen (during the statistics menu selection)
    def overview_user_text():
        return (f"""
User: {usernames[i].capitalize()}
Tasks assigned: {user_tasks[usernames[i]]}
Percentage of tasks assigned to user: {(user_tasks[usernames[i]] / count_tasks) * 100 :.2f}%
Tasks completed: {user_tasks_complete[usernames[i]]}\t\tPercentage complete = {percentage_complete}
Tasks not completed: {user_tasks_not_complete[usernames[i]]}\t\tPercentage not complete = {percentage_not_complete}
Tasks overdue: {user_tasks_overdue[usernames[i]]}\t\tPercentage overdue = {percentage_overdue}
""")

    # variables for task_overview.txt - these are required for the stats in the reports and comparison of dates
    f = open("tasks.txt", "r")
    count_tasks = 0
    count_tasks_not_completed = 0
    count_tasks_overdue = 0
    today_date = date.today() # taken from the import function
    compare_today = today_date.strftime("%Y%m%d")
    compare_today = int(compare_today)
    # format_back = today_format. Needed to make sure that when comparing dates they were in the correct format
    format = "%d %b %Y"  # The format of current due date needed to turn it back into a comparable integer
    
    # variables for user_overview.txt. These are to store the mathematical statistical information requested and display in the reports
    count_reg_users = 0
    user_tasks = {el : 0 for el in usernames}
    user_tasks_complete = {el : 0 for el in usernames}
    user_tasks_not_complete = {el : 0 for el in usernames}
    user_tasks_overdue = {el : 0 for el in usernames}
    # A for loop to take the data from the tasks and perform statistical calculations and comparions to ensure the correct info is being displayed to meet the task
    for line in f: 
        count_tasks += 1
        line = line.replace("\n", "")
        line = line.split(", ")
        if line[5] == "No": # adding up how many tasks have not been completed
            count_tasks_not_completed += 1
        # formating the dates of the tasks and the current date so that they can be compared to see if they are overdue
        compare_due_date = datetime.datetime.strptime(line[4], format) # turns line[4] due date back into a date object with just numbers rather than a string. This also gave a time as well that I got rid of in the next few steps
        compare_due_date = str(compare_due_date) # once they are just numbers turned it into a string so I could tuen it into a list 
        compare_due_date = compare_due_date.split() # turn it into a list to seperate the date and time
        compare_due_date = compare_due_date.pop(0) # pop the date in the list and keep that as a string (removes the time)
        compare_due_date = compare_due_date.replace("-", "") # get rid of any hyphens to turn it into a string of digits example 2022-12-11 becomes 20221211
        compare_due_date = int(compare_due_date) # turn it into an integer for comparing
        if compare_today > compare_due_date and line[5] == "No": # if the task is completed it doesn't add it however if the due date is bigger than the current date it will add one to the counter as an overdue item
            count_tasks_overdue += 1 # add an overdue task to the counter
        if line[0] in user_tasks:
            user_tasks[line[0]] += 1
            if line[5] == "Yes": # adds a counter to the completed tasks
                user_tasks_complete[line[0]] += 1
            else:
                user_tasks_not_complete[line[0]] += 1 # adds one to the cunter if it is not completed
            if compare_today > compare_due_date and line[5] == "No": 
                user_tasks_overdue[line[0]] += 1
            
    if generate_choice == 'task': # if the user is just in the statistics selection. It will print the info to screen (as stated in the capstone 3 pdf)
        print()
        print(overview_tasks_text())        # runs the overview_tasks (nested function) to present it in a nice to read format on the screen)    
    # if the user has gone through either menu option (generate reports or statisitics) it will save it to task_overview.txt file
    if generate_choice == 'both' or generate_choice == 'task': # The capstone 3 pdf wanted the info shown on screen and file for statistics, but on file for generate reports menu selection
        file_task = open ("task_overview.txt", "w+")
        file_task.write(overview_tasks_text()) # follows the overview_tasks_text nested function to make sure it is writing the information to the file in the correct format
        print("\nThe task_overview.txt file has been generated. Please check the file for information.")
        file_task.close()

    # Again this will understand if the user has gone through the generate report or statistics menu items
    if generate_choice == 'both' or generate_choice == 'user': # both options will generate the report in the user_overview.txt file
        file_user = open ("user_overview.txt", "w+") # This will go over any old information with a new report
        file_user.write("USER OVERVIEW\n") # Write this line at the top of the report to sho a header and to start the file fresh
        if generate_choice == 'user':
            print()
            print("USER OVERVIEW")
        # This loop will get the statistics for each user one at a time and collect the information a simple understandable format. 
        # If the program divides by zero (for example the user not having tasks) it will put in N/A insstead
        for i in range(0, len(usernames)):
            try:
                percentage_complete = str(f"{user_tasks_complete[usernames[i]] / user_tasks[usernames[i]] * 100:.2f}%")
            except:
                percentage_complete = "N/A"
            try:
                percentage_not_complete = str(f"{user_tasks_not_complete[usernames[i]] / user_tasks[usernames[i]] * 100:.2f}%")
            except:
                percentage_not_complete = "N/A"
            try:
                percentage_assigned = str(f"{user_tasks[usernames[i]] / count_tasks:.2f}%")
            except:
                percentage_assigned = "N/A"
            try:
                percentage_overdue = str(f"{user_tasks_overdue[usernames[i]] / user_tasks[usernames[i]] * 100:.2f}%")
            except:
                percentage_assigned = "N/A"
            
            file_user.write(overview_user_text()) # This will write the information to the file a user at a time in the correct format as stated in the nested function overview_user_task
            if generate_choice == 'user':
                print(overview_user_text()) # if the report being generated is in statistics then it will also display the information on screen. (However, there could be quite a lot depending on the number of users) 
        print("\nThe user_overview.txt file has been generated. Please check the file for information.")
        file_user.close()
    print()
    f.close()

############# MAIN PROGRAM ##############

# Everytimne you open the program you need to check the latest username and password list to check when logging in
sort_user_pass()
# Run the login process so that the user can get into the main menu_choice.
login()
# If the user has entered a correct username and password the program can proceed into the menu_choice.

# This allows the logged in admin user to see more options to select from, or a basic menu_choice for normal users
# This will loop until the user exits the menu_choice
while True:
    if user == "admin":
        menu_choice = admin_menu()
    else:
        menu_choice = normal_menu()
    
    # Menu choice will decide on which function to run (or exit / try again if required)
    if menu_choice == "r":     # This option adds a new user, it is in both menus as stipulated by the task, but only admin can use it. 
        reg_user() # run the register user function as defined in the capstone 3 project
    elif menu_choice == "a":
        add_task() # run the add task function as defined in the capstone 3 project
    elif menu_choice == "va":
        view_all() # run the view all function as defined in the capstone 3 project
    elif menu_choice == "vm":
        view_mine() # run the register user function as defined in the capstone 3 project
        # this ended up being a large function, but this function was defined in the capstone project pdf
    elif menu_choice == "ds" and user == "admin":
        # Added for compulsary tasks 2. The adminas have a special option to look at statistics.
        # This menu choice ran a lot of the generate reports code. So I kept the simple statisticsa in the main menu choice and ran the generate_reports functions when selected
        # This saved a lot of repeated coding by using the generate_reports function
        user_numbers = 0
        user_tasks = 0
        # Collect the relevant data from the files
        f = open ("user.txt", "r")
        for line in f:
            user_numbers += 1
        f.close()

        f = open ("tasks.txt", "r")
        for line in f:
            user_tasks +=1
        f.close()

        # Print out the statistics amount of users and tasks in a readable format.
        print(f"""
_______________________________________________________________________________________________
Admin - statistics
Total number of users is: {user_numbers}
Total number of tasks is: {user_tasks}
_______________________________________________________________________________________________
    """)
        while True:
            option = input("""Would you like to see the reports:
1 - Task overview
2 - User overview
0 - Back to main menu
Please pick 1,  2, or  0: """)
            if option == '1':
                # if option one is chosen it would change generate_choice to 'tasks' so that it would run certain elements in the generate reports function
                # This would run the task_overview.txt report but also print it to the screen
                generate_choice = 'task'
                generate_reports()
            elif option == '2':
                # If option two is chosen it would change generate_choice to 'user' so that it would run certain elements in the generate reports function
                # This would run the user_overview.txt report but also print it to the screen
                generate_choice = 'user'
                generate_reports()
            elif option == '0': # user needs to type zero to go back to main menu or it will keep looping
                print()
                break
            else:
                print("Not a valid option please try again\n")
     # if the user chooses generate reports, it will change the generate_choice varaiable to 'both' so that only the reports are created and nothing is displayed on the screen
     # This follows the direction of the capstone 3 project about not displaying info on screen for this option
    elif menu_choice == "gr" and user == "admin":
        generate_choice = 'both' 
        generate_reports()

    elif menu_choice == "e":   # Exit Program
        print('Goodbye!')
        exit()
    else:               # If user puts a wrong choice in the menu_choice, it will tell them and they can have another go
        print("You have made a wrong choice, Please try again")


