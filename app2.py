print("=== Task Prioritizer ===")

tasks = []

while True:
    task = input("Enter a task (or type 'done' to finish): ")

    if task.lower() == "done":
        break

    priority = input("Enter priority (high / medium / low): ")

    tasks.append((task, priority))

print("\nYour tasks:")

for t in tasks:
    print(f"- {t[0]} [{t[1]}]")