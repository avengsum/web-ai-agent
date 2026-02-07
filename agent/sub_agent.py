import json
from agent.core import LLMClient
from agent.personas import get_persona
from context.context import ContextManager
import os
from dotenv import load_dotenv
from tool import tool_manager

load_dotenv()


class SubAgent:

  def __init__(self,agent_type,task):
    self.agent_type = agent_type
    self.task = task

    self.ctx = ContextManager()
    self.model = LLMClient(
      api_key=os.getenv("GROQ_API_KEY"),
      model="openai/gpt-oss-20b",
      base_url="https://api.groq.com/openai/v1"
    )

    sys_prompt = get_persona(agent_type)
    self.ctx.add_message("system",sys_prompt)
    self.ctx.add_message("user",f"Your Task: {task}")

  
  def run(self):
    print(f"\n [SUB-AGENT {self.agent_type.upper()}] Starting task: {self.task[:50]}....")


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

        content = res.content
        tool_calls = res.tool_calls
      
      except Exception as e:
        return f"Sub-Agent Crash: {str(e)}"
        
      self.ctx.add_message(
        role="Assitant",
        content=content,
        tool_calls=tool_calls
      )

      if not tool_calls:
        print(f"🤖 [SUB-AGENT] Finished: {content[:50]}...")
        return content
      
      for tc in tool_calls:
        func_name = tc.function.name
        args_str = tc.function.arguments
        tool_id = tc.id

        if func_name == "call_subagent":
          result = "Error subagent cannot call a subagent"
        
        else: 
          print(f"[Sub-agent] running tool {func_name} ....")

          try:
            result = tool_manager.ToolManager.run({
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
          




    