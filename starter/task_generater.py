import csv
import random

max_num_tasks = 168
constraints = ["before", "after"]
tasks = []
total_time_requirement = 0

while total_time_requirement < 84:
    task_name = f"Task {len(tasks)+1}"
    time_requirement = random.randint(1, 8)

    if total_time_requirement + time_requirement > 84:
        continue

    total_time_requirement += time_requirement

    if random.random() < 0.5:
        constraint_type = None
        constraint_task_num = None
    else:
        constraint_type = random.choice(constraints)
        constraint_task_num = random.randint(1, len(tasks)) if constraint_type == "before" else random.randint(len(tasks)+1, max_num_tasks)

    tasks.append({"task_name": task_name, "time_requirement": time_requirement, "constraint_type": constraint_type, "constraint_task_num": constraint_task_num})

while len(tasks) != 168:
    task_name = f"Free time {len(tasks)+1}"
    time_requirement = 1
    constraint_type = None
    constraint_task_num = None
    tasks.append({"task_name": task_name, "time_requirement": time_requirement, "constraint_type": constraint_type, "constraint_task_num": constraint_task_num})

with open("tasks.csv", "w", newline="") as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=["task_name", "time_requirement", "constraint_type", "constraint_task_num"])
    writer.writeheader()
    writer.writerows(tasks)

print(f"Successfully created tasks.csv with {len(tasks)} tasks.")