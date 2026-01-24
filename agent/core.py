import json
from openrouter import OpenRouter
import requests


class LLMClient:
  def __init__(self):
    self.api_key = "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"
    self.model = "mistralai/devstral-2512:free"
    self.base_url = "https://openrouter.ai/api/v1"

  def chat(self,message,max_tokens=2000):

    headers = {
      "Authorization" : f"Bearer {self.api_key}",
      "Content-Type": "application/json"
    }

    data = {
      "model" : self.model,
      "messages" : message,
      "max_tokens" : max_tokens
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



  def chat_stream(self,messages,max_tokens=2000):

    headers = {
      "Authorization" : f"Bearer {self.api_key}",
      "Content-Type": "application/json"
    }

    data = {
      "model" : self.model,
      "messages" : messages,
      "max_tokens" : max_tokens,
      "stream": True

    }

    print("here 1")

    try:
      response = requests.post(
        f"{self.base_url}/chat/completions",
        headers=headers,
        json=data,
        stream=True
      )
      print("here 2")
      response.raise_for_status()

      print("here 3")

      for line in response.iter_lines():
        if line:
          ## because data comes in byte(numbers like 71) so we convert to utf so that we can work
          line = line.decode('utf-8')

          # so strip space ko remove kar deta h like  " hello ".strip()     → "hello"

          ## so iska matlab strp karne ke badd "" empty aai to ise mt lo bs
          if not line.strip():
            continue

         ## so data come likes this
         ## "data: {\"choices\":[{\"delta\":{\"content\":\"Hel\"}}]}"
         ## so the data part is useless so we remove that 
          if line.startswith("data: "):
            line = line[6:]

          elif line.startswith("data:"):
            line = line[5:]

          ## it means ab aur data nahi aaega so break
          if line.strip() == "[DONE]":
            break

          try:
            chunk = json.loads(line)
            
            if 'choices' in chunk and len(chunk['choices']) > 0:
              delta = chunk['choices'][0].get('delta',{})
              content = delta.get('content','')

              if content:
                yield content
          
          except json.JSONDecodeError:
                        # Skip malformed JSON
                 continue
    
    except Exception as e:
      print(f"Error calling OpenRouter: {e}")
      raise


