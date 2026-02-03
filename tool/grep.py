import os

max_file_size = 200 * 1024
max_matches = 50

def grep(path:str,text:str) -> str:

  if not path:
    return "Error: Path is empty"
  
  if not os.path.exists(path):
    return "Error:file does not exists"
  
  if not os.path.isfile(path):
    return "Error: not a file"
  
  if not text:
    return "Error: search is not provided"
  
  if os.path.getsize(path) > max_file_size:
    return "Error: file is too large"
  
  result = []

  try:
    with open(path,"r",encoding="utf-8",errors="replace") as f:
      line_no = 1

      for line in f:
        if text in line:
          result.append(f"{line_no}: {line.rstrip()}")
        
        if len(result) > max_matches:
          break
    
    if not result:
      return "No matches found"
    
    return "\n".join(result)
  
  except Exception as e:
    return f"Error reading files: {str(e)}"