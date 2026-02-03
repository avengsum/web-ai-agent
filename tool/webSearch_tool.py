from ddgs import DDGS

max_results = 5

def webSearch(query:str):
  if not query:
    return "Error: query not provided"
  
  print(f"🕵️  Searching: {query}")
  
  try:
    raw_results = DDGS().text(
        query ,
        region='us-en',
        safesearch='off',
        timelimit='y', 
        page=1, 
        backend="auto",
        max_results=max_results
      )
    
    if not raw_results:
      return f"Error: no search result found for query: {query}"
    
    results = []
    
    query_no = 1

    for data in raw_results:
      title = data.get("title","")
      href = data.get("href","")
      body = data.get("body","")

      results.append(
        f"Result: {query_no}\n"
        f"Title: {title}\n"
        f"URL: {href}\n"
        f"Body: {body}\n"
      )
      query_no += 1
    
    return "\n---\n".join(results)
  
  
  except Exception as e:
    return f"Error: web search tool {str(e)}"
    