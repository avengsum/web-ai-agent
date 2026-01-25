import json
import os
import requests

API_KEY = "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"
MODEL = "mistralai/devstral-2512:free"
URL = "https://openrouter.ai/api/v1/chat/completions"

def list_files(directory="."):
    return "\n".join(os.listdir(directory))

TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "list_files",
            "description": "List files in a directory",
            "parameters": {
                "type": "object",
                "properties": {
                    "directory": {
                        "type": "string",
                        "default": "."
                    }
                },
                "required": []
            }
        }
    }
]

messages = [
    {
        "role": "system",
        "content": "You MUST use tools when asked about files."
    }
]

while True:
    user = input("You: ").strip()
    if user in ["exit", "quit"]:
        break

    messages.append({"role": "user", "content": user})

    raw_tool_calls = []
    full_text = ""

    r = requests.post(
        URL,
        headers={
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        },
        json={
            "model": MODEL,
            "messages": messages,
            "tools": TOOLS,
            "tool_choice": "auto",
            "stream": True
        },
        stream=True
    )

    for line in r.iter_lines():
        if not line:
            continue
        line = line.decode().replace("data:", "").strip()
        if line == "[DONE]":
            break

        chunk = json.loads(line)
        delta = chunk["choices"][0]["delta"]

        if "content" in delta:
            print(delta["content"], end="", flush=True)
            full_text += delta["content"]

        if "tool_calls" in delta:
            raw_tool_calls.extend(delta["tool_calls"])

    print("\n")

    if not raw_tool_calls:
        messages.append({"role": "assistant", "content": full_text})
        continue

    # NORMALIZE
    tool_calls = []
    for tc in raw_tool_calls:
        tool_calls.append({
            "id": tc["id"],
            "type": "function",
            "function": {
                "name": tc["function"]["name"],
                "arguments": tc["function"].get("arguments", "")
            }
        })

    messages.append({
        "role": "assistant",
        "content": full_text,
        "tool_calls": tool_calls
    })

    for tc in tool_calls:
      raw_args = tc["function"].get("arguments", "").strip()
      args = json.loads(raw_args) if raw_args else {}

      result = list_files(args.get("directory", "."))


    messages.append({
            "role": "tool",
            "tool_call_id": tc["id"],
            "content": result
    })
