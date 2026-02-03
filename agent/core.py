import json
import os
import requests
from tool.tool import tool_manager
from dotenv import load_dotenv

load_dotenv()

class LLMClient:
  def __init__(
      self,
      api_key= os.getenv("API_KEY"),
      model = "z-ai/glm-4.5-air:free",
      base_url = "https://openrouter.ai/api/v1"

      ):
    self.api_key = api_key
    self.model = model
    self.base_url = base_url

  def chat(self, message, max_tokens=2000):
    headers = {
      "Authorization" : f"Bearer {self.api_key}",
      "Content-Type": "application/json"
    }

    data = {
      "model" : self.model,
      "messages" : message,
      "max_tokens" : max_tokens,
      "tools": tool_manager.getSchema() ,
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

      return result["choices"][0]["message"]
    
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
      "tools": tool_manager.getSchema(),
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
              
             
              if "tool_calls" in delta:
                yield {
                  "tool_calls": delta["tool_calls"] 
                }
          
          except json.JSONDecodeError:
             continue
    
    except Exception as e:
      print(f"Error calling OpenRouter: {e}")
      raise


