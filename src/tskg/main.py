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

# Removes completed and incomplete from the tasks for easier task recognition
def remove_extra(task):
    return task.replace(incomplete, "").replace(completed, "").strip()

# Adds a task
@app.command()
def add(task: str):
    """
    Adds a task to the To-Do list (Cannot be an existing task)
    """
    tasks = load_tasks()
    if task + incomplete in tasks or task + completed in tasks:
        print("Task has already been added, pick another name")
    else:
        print(f"Added {task} to list")
        tasks.append(task + incomplete)
        save_tasks(tasks)

# Removes a task from the list
@app.command()
def remove(task: str):
    """
    Removes a task from the To-Do list (Must already be on the list)
    """
    tasks = load_tasks()
    for t in tasks:
        if remove_extra(t) == task:
            tasks.remove(t)
            save_tasks(tasks)
            print(f"Removed '{task}' from list")
            return
    print(f"No task named {task} found")

# Completes a task
@app.command()
def complete(task: str):
    """
    Changes the status of a task from "Not Complete" to "Completed"
    """
    tasks = load_tasks()
    for t in tasks:
        if remove_extra(t) and t.endswith(incomplete):
            tasks.remove(t)
            completed_task = remove_extra(task) + completed
            tasks.append(completed_task)
            print(f"Marked {task} as completed")
            removeyn = input("Would you like to remove this task? [Y/n] ")
            if removeyn == "" or str.upper(removeyn) == "Y":
                tasks.remove(completed_task)
                print("Task removed!")
            else:
                print("Task not removed")
            save_tasks(tasks)
            return
    print(f'No incomplete task named {task}')

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
            print(f"{tid}. {task}")
    else:
        print("No tasks found")

