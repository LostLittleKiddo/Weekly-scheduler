import csv
import random

max_num_tasks = 168
tasks = []
total_time_requirement = 0

while total_time_requirement < 168:
    task_name = f"Task {len(tasks)+1}"
    time_requirement = random.randint(1, 8)

    if total_time_requirement + time_requirement > 168:
        time_requirement = 168 - total_time_requirement

    total_time_requirement += time_requirement

    tasks.append({"task_name": task_name, "time_requirement": time_requirement})

print(total_time_requirement)

with open("tasks.csv", "w", newline="") as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=["task_name", "time_requirement"])
    writer.writeheader()
    writer.writerows(tasks)

print(f"Successfully created tasks.csv with {len(tasks)} tasks.")