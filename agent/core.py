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


