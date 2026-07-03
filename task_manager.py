# task_manager.py
# A simple CLI Task Manager for project planning and decision tracking

import json
import os
from datetime import datetime

TASKS_FILE = "tasks.json"

def load_tasks():
    if os.path.exists(TASKS_FILE):
        with open(TASKS_FILE, "r") as f:
            return json.load(f)
    return []

def save_tasks(tasks):
    with open(TASKS_FILE, "w") as f:
        json.dump(tasks, f, indent=2)

def add_task(title, priority="Medium", category="General"):
    tasks = load_tasks()
    task = {
        "id": len(tasks) + 1,
        "title": title,
        "priority": priority,
        "category": category,
        "status": "To Do",
        "created": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "completed": None
    }
    tasks.append(task)
    save_tasks(tasks)
    print(f"✅ Task added: [{priority}] {title}")

def view_tasks(filter_status=None):
    tasks = load_tasks()
    if not tasks:
        print("No tasks found.")
        return
    print(f"\n{'ID':<5} {'Priority':<10} {'Status':<12} {'Category':<15} {'Title'}")
    print("-" * 65)
    for t in tasks:
        if filter_status and t["status"] != filter_status:
            continue
        print(f"{t['id']:<5} {t['priority']:<10} {t['status']:<12} {t['category']:<15} {t['title']}")
    print()

def complete_task(task_id):
    tasks = load_tasks()
    for t in tasks:
        if t["id"] == task_id:
            t["status"] = "Done"
            t["completed"] = datetime.now().strftime("%Y-%m-%d %H:%M")
            save_tasks(tasks)
            print(f"✅ Task {task_id} marked as Done.")
            return
    print(f"Task {task_id} not found.")

def delete_task(task_id):
    tasks = load_tasks()
    tasks = [t for t in tasks if t["id"] != task_id]
    save_tasks(tasks)
    print(f"🗑️ Task {task_id} deleted.")

def summary():
    tasks = load_tasks()
    total = len(tasks)
    done = sum(1 for t in tasks if t["status"] == "Done")
    pending = total - done
    print(f"\n📊 Summary: {total} total | {done} completed | {pending} pending\n")

def main():
    print("🗂️  Project Task Manager")
    print("=" * 40)
    while True:
        print("\n1. Add Task\n2. View All Tasks\n3. View Pending Tasks\n4. Complete Task\n5. Delete Task\n6. Summary\n7. Exit")
        choice = input("Choose an option: ").strip()

        if choice == "1":
            title = input("Task title: ")
            priority = input("Priority (High/Medium/Low) [Medium]: ").strip() or "Medium"
            category = input("Category (e.g. Dev/Design/Testing) [General]: ").strip() or "General"
            add_task(title, priority, category)
        elif choice == "2":
            view_tasks()
        elif choice == "3":
            view_tasks(filter_status="To Do")
        elif choice == "4":
            task_id = int(input("Enter Task ID to complete: "))
            complete_task(task_id)
        elif choice == "5":
            task_id = int(input("Enter Task ID to delete: "))
            delete_task(task_id)
        elif choice == "6":
            summary()
        elif choice == "7":
            print("Goodbye!")
            break
        else:
            print("Invalid option, try again.")

if __name__ == "__main__":
    main()
