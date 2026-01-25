from agent.core import LLMClient
from context import context
from tool.list_file import list_files


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

  test_messages = [
        {"role": "user", "content": "hello"}
    ]
  
  model = LLMClient()
  ctx = context.ContextManager()

  while True:

    user_input = input("You: ").strip()

    if user_input.lower() in ['exit' , 'quit' , 'bye']:
      print("\n goodbye")
      break

    if not user_input:
      continue

    ctx.add_message("user",user_input)

   # The Agent Loop: This allows the AI to call multiple tools in a row
    while True: 
      full_response = ""
      tool_calls = [] # To store any tool requests found in the stream

            # Pass tools=TOOLS_SCHEMA to your chat_stream
      for chunk in model.chat_stream(ctx.get_messages()):
                # If chunk is text, print it
        if isinstance(chunk, str):
            print(chunk, end="", flush=True)
            full_response += chunk
                # If chunk contains a tool call (logic handled in LLMClient)
        elif hasattr(chunk, 'tool_calls'):
            tool_calls.extend(chunk.tool_calls)

      print("\n")

            # CASE A: The AI just talked to you (No tools)
      if not tool_calls:
        ctx.add_message("assistant", full_response)
        break # Wait for next user input

            # CASE B: The AI wants to use a tool
      # Convert tool calls to the format expected by the API
      tool_calls_list = [
        {
          "id": tool.id,
          "type": "function",
          "function": {
            "name": tool.function.name,
            "arguments": tool.function.arguments
          }
        }
        for tool in tool_calls
      ]
      ctx.add_message("assistant", full_response if full_response else None, tool_calls=tool_calls_list)
            
      for tool in tool_calls:
        print(f"--- Running Tool: {tool.function.name} ---")
                
                # Execute the actual Python function
        import json
        try:
          # Parse tool arguments
          args = json.loads(tool.function.arguments) if tool.function.arguments else {}
          directory = args.get("directory", ".")
          
          if tool.function.name == "list_files":
            result = list_files(directory)
          else:
            result = f"Unknown tool: {tool.function.name}"
        except json.JSONDecodeError:
          # If arguments parsing fails, use defaults
          if tool.function.name == "list_files":
            result = list_files()
          else:
            result = f"Unknown tool: {tool.function.name}"
                    
        ctx.add_message("tool", result, tool_call_id=tool.id)

            # After adding tool results, the 'while True' loop repeats,
            # calling the LLM again with the new tool data!


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