import json
import os
from agent.core import LLMClient
from context import context
from tool.edit_file import edit
from tool.read import read_file
from tool.tool import tool_manager
from tool.write import writeFile
from utils import confirm_changes
from utils.compare import compare

model = LLMClient()
ctx = context.ContextManager()

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
  while True:
    user_input = input("You: ").strip()

    if user_input.lower() in ['exit' , 'quit']:
      print("\n goodbye")
      break

    if not user_input:
      continue

    ctx.add_message("user", user_input)

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
        continue

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
            ctx.add_message(role="tool",content="write operation cancelled by user",tool_call_id=tool["id"])
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
          if not new_content or new_content.startswith("Error"):
            ctx.add_message(
              role="tool",
              content=new_content or "Edit failed",
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
            
        ## all other tools
        else:
          result = tool_manager.run(tool)

        print(f"   -> Output: {result}")

        ctx.add_message(role="tool", content=result, tool_call_id=tool["id"])

    except Exception as e:
      print(f"\n❌ Error: {e}\n")

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