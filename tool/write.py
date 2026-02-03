import os

max_content_size = 200 * 1024

avl_mode = ("overwrite","append")

allowed_ext = (".txt",".md",".py",".json",".yaml",".yml",".js","java")

def writeFile(path:str,content:str,mode:str) -> str:

  try:
      ## basic access control

    if not path or ".." in path:
      return "Error: Invalid path"
  
    if not content:
      return "Error: not content provided"
  
    if len(content.encode("utf-8")) > max_content_size:
      return "Error: content size is too large"
  
    if not path.lower().endswith(allowed_ext):
      return "Error: file type not supported"
   
    if mode not in avl_mode:
      return "Error: Invalid mode"
  
  ## files rules
  
    fileExists = os.path.exists(path)

    if fileExists and mode == "overwrite":
      write_mode = "w"
    elif fileExists and mode == "append":
      write_mode = "a"
    elif not fileExists and mode ==    "append":
      return "Errror cannot append because file does not exists" 
    else:
      write_mode = "w"
  
  # write function

    with open(path,write_mode,encoding="utf-8",errors="replace") as f:
      f.write(content)
  
    return f"done: file {path} written mode: {mode}"
  
  except PermissionError:
    return "Error permission denied"
  
  except Exception as e:
    return f"Error writing file: {str(e)}"
  
  
