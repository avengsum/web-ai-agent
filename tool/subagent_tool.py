from agent.sub_agent import SubAgent


def call_subagent(type:str , task:str):

  ## because right now we have only three prompts for subagent
  valid_types = ["coder", "researcher", "general"]

  if type not in valid_types:
    return f"Error: invalid agent type"
  
  sub = SubAgent(agent_type=type,task=task)

  result = sub.run()

  return f"SUB-AGENT RESULT:\n{result}"
