import typer, json
from pathlib import Path

DATA_DIR = Path.home() / "Appdata" / "Local" / "tskgdata"
DATA_DIR.mkdir(parents=True, exist_ok=True)  
DATA_FILE = DATA_DIR / "tasks.json"

app = typer.Typer(help="A simple To-Do list for even simpler people", no_args_is_help=True)

def load_tasks():
    if DATA_FILE.exists():
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return []

def save_tasks(tasks):
    with open(DATA_FILE, "w") as f:
        json.dump(tasks, f, indent=2)

def remove_extra(task):
    return task.replace(" | Not Complete Yet", "").replace(" | Completed!", "").strip()


@app.command()
def add(task: str):
    """
    Adds a task to the To-Do list (Cannot be an existing task)
    """
    tasks = load_tasks()
    if task + " | Not Completed" in tasks or task + " | Completed" in tasks:
        print("Task has already been added, pick another name")
    else:
        print(f"Added {task} to list")
        tasks.append(task + " | Not Completed")
        save_tasks(tasks)


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


@app.command()
def complete(task: str):
    """
    Changes the status of a task from "Not Complete" to "Completed"
    """
    tasks = load_tasks()
    for t in tasks:
        if remove_extra(t) and t.endswith(" | Not Completed"):
            tasks.remove(t)
            completed_task = remove_extra(task) + " | Completed!"
            tasks.append(completed_task)
            save_tasks(tasks)
            print(f"Marked {task} as completed")
            return
    print(f'No incomplete task named {task}')    


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

