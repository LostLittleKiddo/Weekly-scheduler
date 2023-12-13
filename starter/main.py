from tabulate import tabulate
import csv


def import_data_from_csv(csv_file):
    # This function reads a CSV file and converts it into a dictionary.
    # Each row in the CSV file represents a task, with columns for the task name, time requirement, constraint type, and constraint task number.
    # The function returns a dictionary where each key is a task name and each value is another dictionary with keys for the time requirement, constraint type, and constraint task number.
    data_dict = {}

    with open(csv_file, 'r') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            task_name = row['task_name']
            time_requirement = int(row['time_requirement'])
            constraint_type = row['constraint_type']
            constraint_task_num = int(row['constraint_task_num']) if row['constraint_task_num'] else None
            data_dict[task_name] = {'time_requirement': time_requirement, 'constraint_type': constraint_type, 'constraint_task_num': constraint_task_num}

    return data_dict

class Task:
    # The Task class represents a task. Each task has a name, a time requirement, and optionally a constraint type and a constraint task number.
    def __init__(self, name, time_requirement, constraint_type=None, constraint_task_num=None):
        self.name = name
        self.time_requirement = time_requirement
        self.constraint_type = constraint_type
        self.constraint_task_num = constraint_task_num

class Constraint:
    # The Constraint class represents a constraint between two tasks. Each constraint has two tasks and a relation ('before' or 'after').
    def __init__(self, task1, task2, relation):
        self.task1 = task1
        self.task2 = task2
        self.relation = relation  # 'before' or 'after'

class Backtracking:
    # The Backtracking class is used to find a schedule that satisfies all constraints. It has a list of tasks, a list of constraints, a Week object representing the schedule, a set of used tasks, and a counter for the number of attempts to add a task to the schedule.
    def __init__(self, tasks, constraints):
        self.tasks = tasks
        self.constraints = constraints
        self.schedule = Week()
        self.schedule.create_table()
        self.used = set()  # keep track of which tasks have been added to the schedule
        self.attempts = 0  # keep track of the number of attempts to add a task to the schedule

    def backtrack(self):
        if self.schedule.is_full() or self.attempts > 1000:  # add a limit to the number of attempts
            return self.schedule
        for task in self.tasks:
            if task in self.used:  # skip tasks that have already been added
                continue
            for day in range(self.schedule.numday):
                for time in range(12):  # limit the time to 12 hours
                    if self.schedule.can_add_task(day, time, task):  # check if the task can be added
                        self.schedule.add_task_to_schedule(day, time, task)
                        self.used.add(task)
                        self.attempts += 1
                        result = self.backtrack()
                        if result is not None:
                            return result
                        self.schedule.remove_task_from_schedule(day, time, task)
                        self.used.remove(task)
        return None

class AC3:
    # The AC3 class is used to enforce arc consistency. It has a list of tasks and a list of constraints.
    def __init__(self, tasks, constraints):
        self.tasks = tasks
        self.constraints = constraints

    def run(self):
        # The run method initializes a queue with all pairs of different tasks. Then it enters a loop that continues until the queue is empty. In each iteration, it removes a pair of tasks from the queue and revises the domain of the first task. If the domain of the first task becomes empty, it returns False. If the domain of the first task is revised, it adds all pairs of the first task and other tasks to the queue. If the queue becomes empty, it returns True.
        queue = [(task1, task2) for task1 in self.tasks for task2 in self.tasks if task1 != task2]
        while queue:
            task1, task2 = queue.pop(0)
            if self.revise(task1, task2):
                if not task1.domain:
                    return False
                for task3 in self.tasks:
                    if task3 != task1 and task3 != task2:
                        queue.append((task3, task1))
        return True

    def revise(self, task1, task2):
        # The revise method checks each value in the domain of the first task. If the value doesn't satisfy any constraint with any value in the domain of the second task, it removes the value from the domain of the first task. It returns True if the domain of the first task is revised, and False otherwise.
        revised = False
        for value in task1.domain:
            if not any(self.satisfies(task1, value, task2, value2) for value2 in task2.domain):
                task1.domain.remove(value)
                revised = True
        return revised

    def satisfies(self, task1, value1, task2, value2):
        # The satisfies method checks if a value of the first task and a value of the second task satisfy all constraints between the two tasks.
        for constraint in self.constraints:
            if constraint.task1 == task1 and constraint.task2 == task2 and constraint.relation == 'before':
                if value1 >= value2:
                    return False
            if constraint.task1 == task1 and constraint.task2 == task2 and constraint.relation == 'after':
                if value1 <= value2:
                    return False
        return True

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
        return all(slot is not None for day in self.week for slot in day)
    
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


if __name__ == "__main__":
    csv_file_path = 'tasks.csv'
    tasks_dict = import_data_from_csv(csv_file_path)
    tasks = [Task(name, **info) for name, info in tasks_dict.items()]
    constraints = [Constraint(tasks[i], tasks[j], 'before') for i in range(len(tasks)) for j in range(i+1, len(tasks)) if tasks[i].constraint_type == 'before' and tasks[i].constraint_task_num == j]
    constraints += [Constraint(tasks[i], tasks[j], 'after') for i in range(len(tasks)) for j in range(i+1, len(tasks)) if tasks[i].constraint_type == 'after' and tasks[i].constraint_task_num == j]
    backtracking = Backtracking(tasks, constraints)
    schedule = backtracking.backtrack()
    if schedule is not None:
        schedule.print_week()
    else:
        print("No solution found.")