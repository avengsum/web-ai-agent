from agent.sub_agent import SubAgent


def call_subagent(agent_type:str , task_description:str):

  ## because right now we have only three prompts for subagent
  valid_types = ["coder", "researcher", "general"]

  if agent_type not in valid_types:
    return f"Error: invalid agent type"
  
  try:
    sub = SubAgent(agent_type=agent_type,task_description=task_description)

    result = sub.run()

    return f"SUB-AGENT RESULT:\n{result}"
  
  except Exception as e:
      return f"Error running sub-agent: {str(e)}"
