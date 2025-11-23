# main.py
from core.manager import TaskManager, ReminderManager
from core.storage import load_settings

def print_menu():
    print("\n===== TASK FORGE =====")
    print("1. View all tasks")
    print("2. Add task")
    print("3. Add subtask")
    print("4. Complete task")
    print("5. Incomplete task")
    print("6. Toggle reminders ON/OFF")
    print("7. Delete task")
    print("8. View reminders")
    print("0. Exit")
    print("=================================================\n")

def print_task(task, level=0):
    indent="  "*level
    status="✅" if task.completed else "•"
    rem="ON" if task.reminders_enabled else "OFF"
    if task.due_date:
        due=f"(due {task.due_date.strftime('%Y-%m-%d')})"
    else:
        due=""
    print(f"{indent}{status} {task.id} {task.title} [{task.category}] R:{rem}{due}")
    for st in task.subtasks:
        print_task(st,level+1)
def main():
    settings_dict=load_settings().get("ReminderIntervals", {})

    class SettingsWrapper:
        def get_intervals(self, category):
            return settings_dict.get(category.upper(),settings_dict.get(category, [1, 3, 7]))
    settings=SettingsWrapper()
    engine=ReminderManager(settings)
    manager=TaskManager(settings,engine)
    while True:
        print_menu()
        choice=input("Enter your choice: ")
        if choice=="0":
            print("Goodbye!")
            break
        elif choice=="1":
            print("\n--- TASK LIST ---")
            for t in manager.tasks:
                print_task(t)
            print("------------------")
        elif choice=="2":
            title=input("Enter task title: ")
            category=input("Category (STUDY/IMPORTANT/NORMAL/DAILY): ")
            due=input("Due date (YYYY-MM-DD or empty): ")
            if due=="":
                due=None
            rem=input("Enable reminders? (Y/N): ").strip().upper() == "Y"
            t=manager.add_task(title,category,due,rem)
            print(f"Added task: {t.title}")
        elif choice=="3":
            parent_id=input("Enter parent task ID: ")
            title=input("Enter subtask title: ")
            parent=manager.find_task(parent_id)
            if parent:
                category=parent.category
                rem=parent.reminders_enabled
            else:
                category="General"
                rem=True
            st=manager.add_subtask(parent_id,title,category,None,rem)
            print("Subtask added." if st else "Error: Task not found.")
        elif choice=="4":
            taskid=input("Enter task ID to complete: ")
            result=manager.complete_task(taskid)
            if result is None:
                print("Task not found.")
            else:
                print("Task completed.")
                print(f"Reminders created: {len(result)}")
        elif choice=="5":
            taskid=input("Enter task ID: ")
            t=manager.incomplete_task(taskid)
            print("Task marked uncompleted." if t else "Task not found.")
        elif choice=="6":
            taskid=input("Enter task ID: ")
            state=manager.toggle_reminders(taskid)
            if state is None:
                print("Not found.")
            else:
                print("Reminders turned", "ON" if state else "OFF")
        elif choice=="7":
            taskid=input("Enter task ID to delete: ")
            if manager.delete_task(taskid):
                print("Task deleted.")
            else:
                print("Task not found.")
        elif choice=="8":
            print("\n--- REMINDERS ---")
            reminders=engine.list_due()
            if not reminders:
                print("No reminders.")
            for r in reminders:
                date=r.due_on.strftime("%Y-%m-%d")
                done="✓" if r.done else "•"
                print(f"{done} {r.title} = {date}")
            print("------------------")
        else:
            print("Invalid option. Try again.")

if __name__ == "__main__":
    main()