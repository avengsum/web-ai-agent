import json
from agent.core import LLMClient
from context import context
from tool import list_file


def non_streaming():
  print("\n[1] Initializing LLM connections...")

  test_messages = [
        {"role": "user", "content": "hello"}
    ]
  
  model = LLMClient()

  while True:
    user_input = input("prompts:")

    ## exit commnand

    if user_input.lower() in ['exit','quit','bye']:
      print("bye bye")
      break

    if not user_input:
      continue

    test_messages.append({
      "role":"user",
      "content": user_input
    })

    print("Agent: " , end="")

    res = model.chat(test_messages)

    print(res['content'])

    test_messages.append({
      "role":"assistant",
      "content": res['content']
    })


def stream_Res():
  print("\n[1] Initializing LLM connections... for streaming response")
  
  model = LLMClient()
  ctx = context.ContextManager()

  while True:
    user_input = input("You: ").strip()

    if user_input.lower() in ['exit' , 'quit' , 'bye']:
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

      # Case 1: Just text, no tools
      if not tool_calls_buffer:
        ctx.add_message("assistant", full_response)
        continue

      # Case 2: Tools were called
      normalized_tool_calls = list(tool_calls_buffer.values())

      ctx.add_message(
        role="assistant",
        content=full_response if full_response else None,
        tool_calls=normalized_tool_calls
      )

      # Execute Tools
      for tool in normalized_tool_calls:
        try:
          func_name = tool["function"]["name"]
          args_str = tool["function"]["arguments"]
          args = json.loads(args_str) if args_str else {}
          
          print(f"🛠️  Executing: {func_name} | Args: {args}")

          if func_name == "list_files":
            result = list_file.list_files(args.get("directory", "."))
          else:
            result = f"Error: Unknown tool '{func_name}'"

        except json.JSONDecodeError:
           result = "Error: Invalid JSON arguments from AI"
        except Exception as e:
           result = f"Error executing tool: {e}"

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