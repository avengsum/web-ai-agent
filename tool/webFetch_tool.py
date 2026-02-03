import os
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from agent.core import LLMClient

load_dotenv()

def clean_html(html_content):
  soup = BeautifulSoup(html_content,"html.parser")

  for element in soup(["script","style","nav","footer","iframe","svg"]):
    element.decompose()

  lines = []
  for element in soup.descendants:

    if element.name in ['h1', 'h2', 'h3']:
      lines.append(f"\n# {element.get_text().strip()}\n")

    elif element.name == 'p':
      lines.append(element.get_text().strip())

    elif element.name == 'li':
      lines.append(f"- {element.get_text().strip()}")

    elif element.name == 'code':
      lines.append(f"`{element.get_text().strip()}`")

    elif element.name == 'a':
      pass

  
  text = "\n".join(line for line in lines if line)

## to save token we are getting less char
  return text[:10000]

def web_fetch(url:str,question:str):
  print(f"Fetching url : {url}")

  headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
  }


  try:

    ## get html resposne
    respose = requests.get(url,headers=headers,timeout=10)

    respose.raise_for_status()


    ## lets clena it

    clean_text = clean_html(respose.text)

    print(f"content length : {len(clean_text)}")

    if not clean_text.strip():
      return "Error: not abel to get readly html"
    
    print(f"subagent analzying the content of the html for {question}")

    sys_prompt = (
            "You are a Web Scraper Sub-Agent. "
            "Your job is to read the provided Website Content and answer the User's Question. "
            "Ignore navigation, ads, and irrelevant info. "
            "If the answer is found, output it clearly. "
            "If the answer is NOT in the text, say 'Information not found in page'."
        )
    
    user_prompt = f" website content start---\n{clean_text}\n--- website content end ---\n\nQUESTION: {question}"


    client = LLMClient(
      api_key=os.getenv("GROQ_API_KEY"),
      model="openai/gpt-oss-20b",
      base_url="https://api.groq.com/openai/v1"
      )

    messages = [
            {"role": "system", "content": sys_prompt},
            {"role": "user", "content": user_prompt}
        ]
  
    res = client.chat(message=messages)

    if not res:
      print(f"Error: fetch not working")

    answer = res.get("content", "Error: No content from Sub-Agent")

    return f"Source: {url}\n\n{answer}"
  
  except Exception as e:
        return f"Error fetching or parsing web page: {str(e)}"




