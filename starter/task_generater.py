import csv
import random

max_num_tasks = 50

constraints = ["before", "after"]

tasks = []

total_time_requirement = 0

while total_time_requirement < 84:
    task_name = f"Task {len(tasks)+1}"

    time_requirement = random.randint(1, 8)

    new_total_time_requirement = total_time_requirement + time_requirement

    if new_total_time_requirement <= 84:
        if random.random() < 0.5:
            constraint = "None"
        else:
            constraint_type = random.choice(constraints)
            if constraint_type == "before":
                constraint_task_num = random.randint(1, len(tasks))
            else:
                constraint_task_num = random.randint(len(tasks)+1, max_num_tasks)

            constraint = f"{constraint_type} {constraint_task_num}"

        total_time_requirement = new_total_time_requirement

        tasks.append({"task_name": task_name, "time_requirement": time_requirement, "constraint": constraint})

# Open a new CSV file for writing
with open("tasks.csv", "w", newline="") as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=["task_name", "time_requirement", "constraint"])
    writer.writeheader()
    writer.writerows(tasks)

print(f"Successfully created tasks.csv with {len(tasks)} tasks.")