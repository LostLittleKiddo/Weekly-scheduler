from tabulate import tabulate
import csv

class Task:
    """
        This class represents a task with a name and a time requirement.
        Each task also has a domain, which is a list of possible time slots for the task.
    """
    def __init__(self, name, time_requirement):
        self.name = name
        self.time_requirement = time_requirement
        self.domain = list(range(24 - time_requirement + 1))  # possible time slots

class Backtracking:
    """
    This class represents a backtracking algorithm for scheduling tasks.
    It keeps track of the tasks, the schedule, and the sets of used and unused tasks.
    It also counts the number of attempts to add tasks to the schedule.
    """
    def __init__(self, tasks):
        self.tasks = tasks
        self.schedule = Week()
        self.schedule.create_table()
        self.used = set()
        self.unused = set(tasks)  # keep track of unused tasks
        self.attempts = 0

    def print_unused_tasks(self):
        # This function prints the tasks that could not be scheduled due to exceeding the working time limit.
        if self.unused:
            print("The following tasks could not be scheduled due to exceeding the working time limit:")
            for task in self.unused:
                print(f"Task: {task.name}, Time Requirement: {task.time_requirement}")
        else:
            print("All tasks were successfully scheduled.")

    def backtrack(self):
        # This function attempts to find a schedule that fits all tasks.
        # It uses a backtracking algorithm, which tries to add each task to each time slot of each day.
        # If a task cannot be added, it backtracks and tries the next task or time slot.
        if self.schedule.is_full() or self.attempts > 1000:  # add a limit to the number of attempts
            return self.schedule
        for task in self.tasks:
            if task in self.used:  # skip tasks that have already been added
                continue
            for day in range(self.schedule.numday):
                for time in task.domain:  # limit the time to task's domain
                    if self.schedule.can_add_task(day, time, task):  # check if the task can be added
                        self.schedule.add_task_to_schedule(day, time, task)
                        self.used.add(task)
                        self.unused.remove(task)  # remove task from unused set
                        self.attempts += 1
                        result = self.backtrack()
                        if result is not None:
                            return result
                        self.schedule.remove_task_from_schedule(day, time, task)
                        self.used.remove(task)
                        self.unused.add(task)  # add task back to unused set
        return None
class Week:
    def __init__(self):
        # The Week class represents a week schedule. It has a number of days and a number of time slots per day, and a list of lists representing the schedule.
        self.numday = 7
        self.numslot = 24
        self.week = []

    def create_table(self):
        # The create_table method initializes the schedule with None for each time slot of each day.
        for i in range(self.numday):
            self.week.append([])
            for _ in range(self.numslot):
                self.week[i].append(None)

    def is_full(self):
        # The is_full method checks if all time slots of all days are filled.
        
        for day in self.week:
            for slot in day:
                if slot is None:
                    return False

        return True
    
    def can_add_task(self, day, time, task):
        # Check if the task fits in the remaining time slots of the day
        if time + task.time_requirement > self.numslot or time + task.time_requirement > 12:  # added constraint here
            return False
        # Check if all required time slots are free
        for i in range(task.time_requirement):
            if self.week[day][time + i] is not None:
                return False
        return True

    def add_task_to_schedule(self, day, time, task):
        # The remove_task_from_schedule method removes a task from the schedule at a specific day and time.
        # The add_task_to_schedule method adds a task to the schedule at a specific day and time.
        for i in range(task.time_requirement):
            self.week[day][time + i] = task.name  # add the task to the schedule

    def remove_task_from_schedule(self, day, time, task):
        # The print_week method prints the schedule in a tabular format.
        for i in range(task.time_requirement):
            self.week[day][time + i] = None  # remove the task from the schedule

    def print_week(self):
        # The print_week method prints the schedule in a tabular format.
        days_of_week = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        time_slots = []
        print_list = []

        for start, end in zip(range(0, 24), range(1, 25)):
            time_slot = f"{start:02d}:00-{end:02d}:00"
            time_slots.append(time_slot)

        for time_slot in time_slots:
            row = [time_slot] + [None] * len(days_of_week)
            print_list.append(row)

        for i in range(self.numday):
            for j in range(self.numslot):
                if self.week[i][j] != None:
                    print_list[j][i+1] = self.week[i][j]
                else: 
                    print_list[j][i+1] = "No work :D"

        headers = [" "] + days_of_week
        print(tabulate(print_list, headers=headers, tablefmt="grid"))

def import_data_from_csv(csv_file):
    # This function imports task data from a CSV file.
    # It opens the file, reads it line by line using a CSV reader,
    # and adds each task to a dictionary with the task name as the key and the time requirement as the value.
    data_dict = {}

    with open(csv_file, 'r') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            task_name = row['task_name']
            time_requirement = int(row['time_requirement'])
            data_dict[task_name] = {'time_requirement': time_requirement}

    return data_dict

def make_task(tasks_dict):
    # This function creates Task objects from a dictionary of tasks.
    # It iterates over the items in the dictionary, creates a Task object for each one,
    # and adds the Task object to a list.
    tasks = []

    for name, info in tasks_dict.items():
        task = Task(name, **info)
        tasks.append(task)
    return tasks

if __name__ == "__main__":
    # This is the main function that is executed when the script is run.
    # It imports task data from a CSV file, creates Task objects from the data,
    # creates a Backtracking object with the tasks, and attempts to create a schedule.
    # If a schedule is found, it prints the schedule.
    csv_file_path = 'tasks.csv'
    tasks_dict = import_data_from_csv(csv_file_path)
    tasks = make_task(tasks_dict)
    backtracking = Backtracking(tasks)
    schedule = backtracking.backtrack()
    if schedule is not None:
        schedule.print_week()
        backtracking.print_unused_tasks()
    else:
        print("No solution found.")