class Task:
    def __init__(self, name, time_requirement, constraint):
        self.name = name
        self.time_requirement = time_requirement
        self.constraint = constraint

def parse_csv(filename):
    tasks = []
    with open(filename, 'r') as f:
        for line in f.readlines()[1:]:
            name, time_requirement, constraint = line.strip().split(',')
            time_requirement = int(time_requirement)
            constraint = constraint.strip() or None
            tasks.append(Task(name, time_requirement, constraint))
    return tasks

def parse_constraint(constraint):
    if constraint is None:
        return None
    parts = constraint.split()
    if parts[0] == 'before':
        return (parts[1], 'before', int(parts[2]))
    elif parts[0] == 'after':
        return (parts[1], 'after', int(parts[2]))
    else:
        raise ValueError(f"Invalid constraint: {constraint}")

def ac3(tasks, constraints):
    """
    Applies AC-3 algorithm to enforce arc consistency.
    """
    queue = [(task, constraint) for task in tasks for constraint in constraints if task != constraint[0]]
    while queue:
        task, constraint = queue.pop(0)
        if revised(task, constraint, tasks, constraints):
            for c in constraints:
                if c[0] == task and c != constraint:
                    queue.append((c[0], c))

def revised(task, constraint, tasks, constraints):
    revised = False
    for value in task.domain:
        valid = False
        for other_value in tasks[constraint[1]].domain:
            if satisfies(value, constraint, other_value):
                valid = True
                break
        if not valid:
            task.domain.remove(value)
            revised = True
    return revised

def satisfies(value1, constraint, value2):
    if constraint[2] == 'before':
        return value1 < value2
    elif constraint[2] == 'after':
        return value1 >= value2 + tasks[constraint[1]].time_requirement
    else:
        return True

def backtracking_search(tasks, constraints, assignments):
    if all(task.assigned for task in tasks):
        return assignments
    unassigned = next(task for task in tasks if not task.assigned)
    for value in unassigned.domain:
        if consistent(value, assignments, constraints):
            unassigned.assign(value)
            assignments.append(unassigned)
            result = backtracking_search(tasks, constraints, assignments)
            if result is not None:
                return result
            unassigned.unassign()
            assignments.pop()
    return None

def consistent(value, assignments, constraints):
    for assigned in assignments:
        if assigned == value:
            return False
        for constraint in constraints:
            if assigned.name == constraint[0] and value == constraint[1]:
                return False
            if assigned.name == constraint[1] and assigned.assigned_value + assigned.time_requirement > value:
                return False
    return True

def print_schedule(tasks, days=7):
    for day in range(days):
        print(f"Day {day+1}:")
        for hour in range(24):
            tasks_for_hour = [task for task in tasks if task.assigned_value == hour]
            if tasks_for_hour:
                print(f"\t{hour+1}:00 - {hour+2}:00: {', '.join(task.name for task in tasks_for_hour)}")

def main():
    tasks = parse_csv("tasks.csv")
    constraints = [parse_constraint(task.constraint) for task in tasks]
    for task in tasks:
        task.domain = list(range(24))
    ac3(tasks, constraints)
    assignments = []
    schedule = backtracking_search(tasks, constraints, assignments)
    if schedule is None:
        print("No solution found.")
    else:
        print_schedule(tasks)

if __name__ == "__main__":
    main()
