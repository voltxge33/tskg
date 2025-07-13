#Imports
import typer, json
from pathlib import Path

#Task Storing Variables and the like
DATA_DIR = Path.home() / "Appdata" / "Local" / "tskgdata"
DATA_DIR.mkdir(parents=True, exist_ok=True)
DATA_FILE = DATA_DIR / "tasks.json"

# TYPER MY BELOVED
app = typer.Typer(help="A simple To-Do list for even simpler people", no_args_is_help=True)
# Variables so I don't have to type the same exact fucking thing 10 times
completed = " | Completed!"
incomplete = " | Not Completed"

# Retrieves all tasks on json file
def load_tasks():
    if DATA_FILE.exists():
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return []

# Saves the updated task list after a removal or an addition.
def save_tasks(tasks):
    with open(DATA_FILE, "w") as f:
        json.dump(tasks, f, indent=2)


# Adds a task
@app.command()
def add(task: str = typer.Argument(..., help="The name of the task you want to add"),
        note: str = typer.Option("", help='If you want to add a specific note to further describe'),
        priority: str = typer.Option("", help="Priorities (High, Medium, Low, H, M, L)")):
    """
    Adds a task to the To-Do list (Cannot be an existing task)
    """
    if priority:
        if str.lower(priority) in ('h', 'high'):
            priority = "High"
        elif str.lower(priority) in ("l", 'low'):
            priority = "Low"
        elif str.lower(priority) in ("m", "medium"):
            priority = "Medium"
        else:
            print(f"{priority} is not a correct priority level (L,M,H, Low, Medium, High)")
            return
    tasks = load_tasks()
    new_task = {
        "name": task,
        "status": incomplete,
        "note": note,
        "priority": priority
    }
    if any(t["name"].lower() == task.lower() for t in tasks):
        print(f"{task} already in list, please try again.")
        return
    tasks.append(new_task)
    save_tasks(tasks)
    print(f'{task} added to the list.')

# Removes a task from the list
@app.command()
def remove(task: str):
    """
    Removes a task from the To-Do list (Must already be on the list)
    """
    tasks = load_tasks()
    for t in tasks:
        if t["name"] == task:
            tasks.remove(t)
            save_tasks(tasks)
            print(f'Removed {task} from list')
            return
    print(f"{task} not found in list, try again.")


# Completes a task
@app.command()
def complete(task: str):
    """
    Changes the status of a task from "Not Complete" to "Completed"
    """
    tasks = load_tasks()
    for t in tasks:
        if t["name"] == task:
            if t["status"] == completed:
                print(f"{task} is already completed")
                return
            t["status"] = completed
            print(f'Marked {task} as completed')
            removeyn = input("Would you like to remove this task? [Y/n] ").strip().lower()
            if removeyn in ["", "y", "yes"]:
                tasks.remove(t)
                print("Task removed!")
            else:
                print("Task not removed.")
            save_tasks(tasks)
            return
    print(f"{task} not found in list.")


# Lists all current tasks
@app.command()
def list():
    """
    Lists all tasks in list
    """
    tasks = load_tasks()
    if tasks:
        print("Tasks:")
        for tid, task in enumerate(tasks, start=1):
            if task["note"] != "" and task["priority"] != "":
                print(f"{tid}. {task['name']}{task['status']}\nNote: {task['note']}\nPriority: {task['priority']}")
            elif task["note"] != "":
                print(f"{tid}. {task['name']}{task['status']}\nNote: {task['note']}")
            elif task["priority"] != "":
                print(f"{tid}. {task['name']}{task['status']}\nPriority: {task['priority']}")
            else:
                print(f"{tid}. {task['name']}{task['status']}")
    else:
        print("No tasks found")

if __name__ == "__main__":
    app()
