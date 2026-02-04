import json
import os
from datetime import datetime

state = ".agent_state.json"

class TaskManager:
  def __init__(self):
    self.tasks = []

  
  def load_state(self):
    if os.path.exists(state):

      try:
        with open(state,"r") as f:
          self.tasks = json.load(f)
      except:
        self_task = []
  
  def save_state(self):
    with open(state,"w") as f:
      json.dump(self.tasks,f,indent=2)
  
  def add_todo(self,task:str,dependencies: list = None):
    new_id = len(self.tasks) + 1

    self.tasks.append({
      "id":new_id,
      "task":task,
      "status": "PENDING",
      "dependencies": dependencies or [],
      "verification": None 
    })

    self.save_state()
    return f"Task {new_id} added: {task}"
  
  def update_todo(self,task_id: int , status: str, notes: str = ""):
    for t in self.tasks:
      if t["id"] == task_id:
        t["status"] == status

        if notes:
          t["notes"] = notes
        
        self.save_state()
        return f"Task {task_id} updated to {status}"
      
    return f"Error: Task {task_id} not found"
  
  def mark_done(self,task_id: int, verification:str):
    for t in task_id:
      if t["id"] == task_id:
        t["status"] = "COMPLETED"
        t["verification"] = verification
        self.save_state()
        return f"Task {task_id} COMPLETED. Proof: {verification}"
    return f"Error: Task {task_id} not found"
  
  def get_system_prompt_addition(self):
        """
        Creates a markdown representation of the state for the System Prompt.
        """
        if not self.tasks:
            return "\n[PLAN STATUS]: No plan yet. You MUST use 'add_todo' to create a plan."
        
        prompt = "\n[CURRENT PROJECT PLAN]\n"
        prompt += "| ID | Status | Task | Dependencies |\n"
        prompt += "|--- |--- |--- |--- |\n"
        
        for t in self.tasks:
            # Optimization: If completed, summarize slightly
            status_icon = "✅" if t['status'] == 'COMPLETED' else "⏳" if t['status'] == 'PENDING' else "🚧"
            deps = str(t['dependencies']) if t['dependencies'] else "None"
            prompt += f"| {t['id']} | {status_icon} {t['status']} | {t['task']} | {deps} |\n"
        
        return prompt

  
