from agent.core import LLMClient


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
      "role":"system",
      "content": res['content']
    })



def stream_Res():
  print("\n[1] Initializing LLM connections... for streaming response")

  test_messages = [
        {"role": "user", "content": "hello"}
    ]
  
  model = LLMClient()

  while True:

    user_input = input("You: ").strip()

    if user_input.lower() in ['exit' , 'quit' , 'bye']:
      print("\n goodbye")
      break

    if not user_input:
      continue

    test_messages.append({
      "role":"user",
      "content":user_input
    })

    try:
      full_resposne = ""

      for chunk in model.chat_stream(test_messages):
        print(chunk,end="" ,flush=True)

        full_resposne +=chunk

      print("\n")

      test_messages.append({
        "role":"system",
        "content":full_resposne
      })

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