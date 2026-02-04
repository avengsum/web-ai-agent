import json
import os
from agent.core import LLMClient
from agent.task_manager import TaskManager
from context import context
from tool import grep
from tool.edit_file import edit
from tool.execute_cmd import exe_cmd
from tool.glob import glob_files
from tool.read import read_file
from tool.tool import tool_manager
from tool.webFetch_tool import web_fetch
from tool.webSearch_tool import webSearch
from tool.write import writeFile
from utils import confirm_changes
from utils.cmd_confirm import cmdConfirm
from utils.compare import compare
import time
from dotenv import load_dotenv

load_dotenv()

model = LLMClient(api_key=os.getenv("GROQ_API_KEY"),model="openai/gpt-oss-120b",base_url="https://api.groq.com/openai/v1")

ctx = context.ContextManager()

task = TaskManager()

def non_streaming():
  print("\n[1] Initializing LLM connections...")

  while True:
    user_input = input("prompts:")

    ## exit commnand

    if user_input.lower() in ['exit','quit']:
      print("bye bye")
      break

    if not user_input:
      continue

    ctx.add_message(
      role="user",
      content=user_input
    )

    res = model.chat(ctx.get_messages())

    ## no tool called

    if 'tool_calls' not in res:
      print("Agent:", res["content"])
      ctx.add_message(
      role="assistant",
      content=res["content"] 
      )
      continue

    ctx.add_message(
      role="assistant",
      content=res["content"],
      tool_calls=res["tool_calls"]
    )

    for tool_call in res["tool_calls"]:
      # before tool manger

      tool_id = tool_call["id"]
      # func_name = tool_call["function"]["name"]
      # args = json.loads(tool_call["function"]["arguments"] or "{}")
      
      # if func_name == "list_files":
      #   result = list_file.list_files(args.get("directory","."))

      # else:
      #   result = f"Error: Unknown tool '{func_name}'"
      
      result = tool_manager.run(tool_call)

      ## send tool result back
      ctx.add_message(role="tool", 
                    content=result,
                    tool_call_id=tool_id
        )
  
    ## now again send a request so that we can get result

    tool_result = model.chat(ctx.get_messages())

    print("Agent:", tool_result["content"])
    ## now add this response also 
    ctx.add_message(
      role="assistant",
      content=tool_result["content"]
    )
    

def stream_Res():
  print("\n[1] Initializing LLM connections... for streaming response")
  ## so this outer loop is for contouns question asking
  while True:
    user_input = input("You: ").strip()

    if user_input.lower() in ['exit' , 'quit']:
      print("\n goodbye")
      break

    if not user_input:
      continue

    plan_status = task.get_task_prompt()
    full_system_prompt = context.SYSTEM_PROMPT + "\n" + plan_status

    ctx.add_message("system", full_system_prompt)

    ctx.add_message("user", user_input)

    ## this inner is for continuos ai agent tool kare aur usk response se phir new tool
    ## kare so its true agentic loop ot will make them learn and apply

    while True:
       try:
        full_response = ""
        # Buffer to accumulate partial tool chunks
        tool_calls_buffer = {} 
      
        print("AI: ", end="", flush=True)

        for chunk in model.chat_stream(ctx.get_messages()):
          if isinstance(chunk, str):
            print(chunk, end="", flush=True)
            full_response += chunk
        
          elif isinstance(chunk, dict) and "tool_calls" in chunk:
            for tc_chunk in chunk["tool_calls"]:
              index = tc_chunk["index"]
            
              # Initialize buffer for this index if not exists
              if index not in tool_calls_buffer:
                tool_calls_buffer[index] = {
                "id": "",
                "type": "function",
                "function": { "name": "", "arguments": "" }
              }
            
              # Combine the chunks
              if "id" in tc_chunk:
               tool_calls_buffer[index]["id"] += tc_chunk["id"]
            
               if "function" in tc_chunk:
                if "name" in tc_chunk["function"]:
                  tool_calls_buffer[index]["function"]["name"] += tc_chunk["function"]["name"]
                if "arguments" in tc_chunk["function"]:
                  tool_calls_buffer[index]["function"]["arguments"] += tc_chunk["function"]["arguments"]

        print("\n") 

        # Case1:text no tools 
        if not tool_calls_buffer:
          ctx.add_message("assistant", full_response)
          break  ## ye break is liye kyuki ab agent ko call karne ke liye kuch nahi so break
        ## the loop

         # Case2: Tools call
        normalized_tool_calls = list(tool_calls_buffer.values())

        ctx.add_message(
          role="assistant",
          content=full_response if full_response else None,
          tool_calls=normalized_tool_calls
         )

         # Execute Tools
        for tool in normalized_tool_calls:
        # before tool manager
        
    #     func_name = tool["function"]["name"]
    #     args_str = tool["function"]["arguments"]
    #     args = json.loads(args_str) if args_str else {}

    #     print(f"🛠️  Executing: {func_name} | Args: {args}")

    #     if func_name == "list_files":
    #         result = list_file.list_files(args.get("directory", "."))
    #     elif func_name == "read_file":
    #         result = read.read_file(args.get("path"))
    #     else:
    #         result = f"Error: Unknown tool '{func_name}'"

    # except json.JSONDecodeError:
    #     result = "Error: Invalid JSON arguments from AI"
    # except Exception as e:
    #     result = f"Error executing tool: {e}"

    ## specially for write tool because of confimation function
         tool_name = tool["function"]["name"]
         args = json.loads(tool["function"]["arguments"] or "{}")

         if tool_name == "write_file":
          path = args.get("path")
          new_content = args.get("content")
          mode = args.get("mode")

          if path and os.path.exists(path):
            old_content = read_file(path)

          else:
            old_content = ""

          print("this is write tool")

          diff = compare(old_content,new_content,path)

          if diff == "No changes":
            print("No changes detected so no write operation")

            ctx.add_message(role="tool",content="No changes",tool_call_id=tool["id"])
            continue

          if not confirm_changes.confirmChanges(diff):
            print("user deciled changes")
            ctx.add_message(
              role="tool",
              content="write operation cancelled by user",
              tool_call_id=tool["id"]
              )
            continue

          result = writeFile(path,new_content,mode)
          print(result)

          ctx.add_message(
            role="tool",
            content=result,
            tool_call_id=tool["id"]
          )

         elif tool_name == "edit_file":
          print("this is edit tool")
          path = args.get("path")
          search = args.get("search")   
          replace = args.get("replace")
          print(f"search : {search}")
          print(f"replace : {replace}")
          
          old_content = read_file(path)

          if not old_content or old_content.startswith("Error"):
              old_content = ""

          new_content = edit(path, search=search, replace=replace)
          if not new_content or new_content.startswith("Error") or new_content == "No changes made":
            result_msg = new_content if new_content else "Error: Edit failed (unknown reason)"
            ctx.add_message(
              role="tool",
              content=result_msg,
              tool_call_id=tool["id"]
            )
            continue

          diff = compare(old_content,new_content,path)

          if diff == "No changes":
            print("No Changes detected")

            ctx.add_message(
              role="tool",
              content="No changes",
              tool_call_id=tool["id"]
            )
            continue

          if not confirm_changes.confirmChanges(diff):
            print("user decliled changes")

            ctx.add_message(
              role="tool",
              content="edit operation cancelled by user",
              tool_call_id=tool["id"]
            )
            continue

          result = writeFile(path,new_content,"overwrite")

          print(result)

          ctx.add_message(
            role="tool",
            content=result,
            tool_call_id=tool["id"]
          )

          continue
            
         elif tool_name == "execute_command":
            command = args.get("command")


            if not cmdConfirm(command):
              print("User do not want the agent to run the command")
              ctx.add_message(
               role="tool",
               content="User do not want the agent to run the command",
               tool_call_id=tool["id"]
              )
              continue

            result = exe_cmd(command)

            ctx.add_message(
               role="tool",
               content=result,
               tool_call_id=tool["id"]
            )
            continue
         
         elif tool_name == "glob":
           pattern = args.get("pattern")

           print("using glob")

           result = glob_files(pattern)

           ctx.add_message(
             role="tool",
             content=result,
             tool_call_id=tool["id"]
           )
           continue
         
         elif tool_name == "grep":
           path = args.get("path")
           text = args.get("text")

           print(f"using grep on {path}")

           result = grep.grep(path=path,text=text)

           ctx.add_message(
             role="tool",
             content=result,
             tool_call_id=tool["id"]  
           )
           continue
          
         elif tool_name == "webSearch":
           query = args.get("query")

           result = webSearch(query)

           ctx.add_message(
             role="tool",
             content=result,
             tool_call_id=tool["id"]
           )
           continue
         
        #  elif tool_name == "web_fetch":
        #    url = args.get("url")
        #    question = args.get("question")


        #    result = web_fetch(url=url,question=question)

        #    ctx.add_message(
        #      role="tool",
        #      content= result,
        #      tool_call_id=tool["id"]
        #    )
        #    continue
           

        ## all other tools
        else:
          print(f"🛠️  Running Tool: {tool_name}")

          result = tool_manager.run(tool)

        print(f"   -> Output: {result}")

        ctx.add_message(role="tool", content=result, tool_call_id=tool["id"])

        time.sleep(2)
       
       except Exception as e:
        print(f"\n❌ Error: {e}\n")
        break

    
def choose_mode():
    """Let user choose between streaming and non-streaming"""
    print("=" * 60)
    print("🤖 AI Coding Agent")
    print("=" * 60)
    print("\nChoose response mode:")
    print("1. Non-Streaming (complete response at once)")
    print("2. Streaming (word-by-word, like ChatGPT)")

    while True:
      choice = input("\nEnter 1 or 2").strip()

      if choice == '1':
        return False
      elif choice == '2':
        return True
      else:
        print("invalid choose between 1 or 2")

def main():
  streaming = choose_mode()

  if streaming:
    stream_Res()
  else:
    non_streaming()

main()