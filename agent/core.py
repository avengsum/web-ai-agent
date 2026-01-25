import json
from tool.tool import tools
from openrouter import OpenRouter
import requests


class LLMClient:
  def __init__(self):
    self.api_key = "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"
    self.model = "mistralai/devstral-2512:free"
    self.base_url = "https://openrouter.ai/api/v1"

  def chat(self, message, max_tokens=2000):
    headers = {
      "Authorization" : f"Bearer {self.api_key}",
      "Content-Type": "application/json"
    }

    data = {
      "model" : self.model,
      "messages" : message,
      "max_tokens" : max_tokens,
      "tools": tools,
      "tool_choice" : "auto"
    }

    try: 
      response = requests.post(
        f"{self.base_url}/chat/completions",
        headers=headers,
        json=data
      )
      response.raise_for_status()
      result = response.json()

      return{
        "content" : result['choices'][0]['message']['content']
      }
    except Exception as e:
      print(f"Error calling OpenRouter: {e}")
      raise

  def chat_stream(self, messages, max_tokens=2000):
    headers = {
      "Authorization" : f"Bearer {self.api_key}",
      "Content-Type": "application/json"
    }

    data = {
      "model" : self.model,
      "messages" : messages,
      "max_tokens" : max_tokens,
      "stream": True,
      "tools": tools,
      "tool_choice" : "auto"
    }

    try:
      response = requests.post(
        f"{self.base_url}/chat/completions",
        headers=headers,
        json=data,
        stream=True
      )
      response.raise_for_status()

      for line in response.iter_lines():
        if line:
          line = line.decode('utf-8')
          if not line.strip():
            continue

          if line.startswith("data: "):
            line = line[6:]
          elif line.startswith("data:"):
            line = line[5:]

          if line.strip() == "[DONE]":
            break

          try:
            chunk = json.loads(line)
            
            if 'choices' in chunk and len(chunk['choices']) > 0:
              delta = chunk['choices'][0].get('delta',{})
              
              if "content" in delta:
                yield delta["content"]
              
              # --- VITAL FIX BELOW ---
              if "tool_calls" in delta:
                # We check specifically for the key to avoid the error
                yield {
                  "tool_calls": delta["tool_calls"] 
                }
              # -----------------------
          
          except json.JSONDecodeError:
             continue
    
    except Exception as e:
      print(f"Error calling OpenRouter: {e}")
      raise


