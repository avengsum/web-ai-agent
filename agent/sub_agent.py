import json
from agent.personas import get_persona
from context.context import ContextManager
import os
from dotenv import load_dotenv


load_dotenv()


class SubAgent:

  def __init__(self,agent_type,task_description):
    from tool.tool import tool_manager
    from agent.core import LLMClient


    self.agent_type = agent_type
    self.task_description = task_description
    self.ctx = ContextManager()
    self.tool_manager = tool_manager
    self.model = LLMClient(
      api_key=os.getenv("GROQ_API_KEY"),
      model="openai/gpt-oss-20b",
      base_url="https://api.groq.com/openai/v1"
    )

    sys_prompt = get_persona(agent_type)
    self.ctx.add_message("system",sys_prompt)
    self.ctx.add_message("user",f"Your Task: {task_description}")

  
  def run(self):
    print(f"\n [SUB-AGENT {self.agent_type.upper()}] Starting task: {self.task_description[:50]}....")


    ## limint the loop to prevet infinite
    max_turn = 10

    turn = 0

    while turn < max_turn:
      turn +=1

      ## chat with subagent
      try:

        res = self.model.chat(
          message = self.ctx.get_messages()
        )

        if isinstance(res, dict):
            content = res.get("content")
            tool_calls = res.get("tool_calls")
        else:
            content = res.content
            tool_calls = res.tool_calls
      
      except Exception as e:
        return f"Sub-Agent Crash: {str(e)}"
        
      self.ctx.add_message(
        role="assitant",
        content=content,
        tool_calls=tool_calls
      )

      if not tool_calls:
        print(f"🤖 [SUB-AGENT] Finished: {content[:50]}...")
        return content
      
      for tc in tool_calls:
        if isinstance(tc, dict):
            # for Dictionary
            func_name = tc["function"]["name"]
            args_str = tc["function"]["arguments"]
            tool_id = tc["id"]
        else:
            func_name = tc.function.name
            args_str = tc.function.arguments
            tool_id = tc.id

        if func_name == "call_subagent":
          result = "Error subagent cannot call a subagent"
        
        else: 
          print(f"[Sub-agent] running tool {func_name} ....")

          try:
            result = self.tool_manager.run({
              "function":{"name": func_name, "arguments" : args_str
                          }
            })
          
          except Exception as e:
            result = f"Error: {str(e)}"
      
      self.ctx.add_message(
            role="tool",
            content=str(result),
            tool_call_id=tool_id
        )
  
    return "Error: subaget reached max turn limit without finishing"
          




    