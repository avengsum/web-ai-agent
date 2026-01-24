import tiktoken

system_prompts = """You are an AI assistant designed to help with a wide range of tasks, including coding, research, writing, and problem solving. Always prioritize accuracy, never guess information, and request missing data before proceeding. When working with files, only read them if necessary, and never assume their contents. Only write files when you have clear instructions and fully verified content. Use available tools whenever needed and always provide structured output in JSON when interacting with tools. Explain your reasoning before taking any action and plan your steps carefully for multi-step tasks. Stop when the task is complete or when additional input from the user is required. Communicate clearly, ask clarifying questions if instructions are ambiguous, and provide precise, actionable guidance without unnecessary assumptions."""

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

  def manage_context(self):
    total_tokens = 0 

    for message in self.history:
      text = message['content']
      token = self.count_tokens(text)
      # print(f"Message: {text} -> Tokens: {token}")
      total_tokens+=token
      # print(f"totaltoken: {total_tokens}")

    while total_tokens > self.max_tokens and len(self.history) > 2:
      removed = self.history.pop(1)
      total_tokens -= self.count_tokens(removed['content'])
      print(f"DEBUG: Context Manager pruned an old message to save space.")
  
  def get_messages(self):
    return self.history



    