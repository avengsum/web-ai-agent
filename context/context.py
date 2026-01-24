import tiktoken
from propmts.system import system_prompts


class ContextManager:
  def __init__(self,max_tokens=2048,system_prompt=system_prompts):
    self.max_tokens = max_tokens
    self.model = "mistralai/devstral-2512:free"
    self.history = [{"role": "system", "content": system_prompt}]
    self.encoding = tiktoken.get_encoding("cl100k_base")

  
  def count_tokens(self,text):
    return len(self.encoding.encode(text))
  
  def add_message(self,role,content):
    self.history.append({
      "role":role,
      "content":content
    })
    self.manage_context()

  def manage_contex(self):
    total_tokens = 0 

    for message in self.history:
      text = message['content']
      token = self.count_tokens(text)
      print(f"Message: {text} -> Tokens: {token}")
      total_tokens+=token

    while total_tokens > self.max_tokens and len(self.history) > 2:
      removed = self.history.pop(1)
      total_tokens -= self.count_tokens(removed['content'])
      print(f"DEBUG: Context Manager pruned an old message to save space.")
  
  def get_messages(self):
    return self.history



    