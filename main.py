from agent.core import LLMClient


def main():
  print("\n[1] Initializing LLM connections...")

  test_messages = [
        {"role": "user", "content": "Say 'I am ready to code!' and nothing else."}
    ]
  
  model = LLMClient()
  res = model.chat(test_messages)

  print(res)

main()