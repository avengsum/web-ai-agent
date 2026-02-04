from agent.task_manager import TaskManager


task_manager = TaskManager

def add_todo(task: str, dependencies: str = ""):
    """
    Added a new pask.
    dependencies: comma for separating id (e.g. "1, 2")
    """
    dep_list = [int(x.strip()) for x in dependencies.split(",")] if dependencies else []
    return task_manager.add_todo(task, dep_list)

def update_status(task_id: int, status: str, notes: str = ""):
    """
    Update a task status. 
    Status must be: PENDING, IN_PROGRESS, FAILED
    """
    valid_status = ["PENDING", "IN_PROGRESS", "FAILED"]
    if status not in valid_status:
        return f"Error: Status must be one of {valid_status}"
    return task_manager.update_todo(task_id, status, notes)

def mark_done(task_id: int, verification: str):
    """
    Mark a task as COMPLETED.
    verification: to check is it done
    """
    return task_manager.mark_done(task_id, verification)