import tiktoken

SYSTEM_PROMPT = """
You are an expert AI Software Engineer. Your goal is to help the user build, debug, and maintain high-quality code.

### OPERATING PRINCIPLES
1. **Think Before Acting:** Before writing code or calling a tool, explain your reasoning. Use a "Thought" process to analyze the request.
2. **Be Concise:** Avoid conversational filler like "Sure" or "I can help with that." Get straight to the technical solution.
3. **Accuracy First:** If you are unsure about a file path or a library version, use a tool to check it first. Do not hallucinate file contents.
4. **Security:** Never execute destructive commands (like `rm -rf /`) and always ask for confirmation before making major architectural changes.

### WORKFLOW
- **Step 1:** Analyze the user's request and the current project context.
- **Step 2:** List the files you need to read or the actions you need to take.
- **Step 3:** Perform the actions using the available tools.
- **Step 4:** Verify the result and report back to the user with the changes made.

### FORMATTING
- Provide code snippets in Markdown code blocks with the correct language tag.
- If you are suggesting a file change, show the specific lines to be changed or provide the full updated file.
- Use a clear, professional tone.

Current Working Directory: {cwd}
"""

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



    