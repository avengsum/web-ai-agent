import os

max_file_size = 200 * 1024 # 200 kb

binary_ext = (".png",".jpg",".jpeg",".gif",".pdf")

def read_file(path: str) -> str:
  try:
    if not path or ".." in path:  ## .. means path travesel so it should not do that
      return "Error: Invalid file path"
    
    if not os.path.exists(path):
      return "Error: File not found"
    
    if not os.path.isfile(path):
      return "Error: path is not file"
    
    if path.lower().endswith(binary_ext):
      return "Error: unsupported file type"
    
    size = os.path.getsize(path)

    if size > max_file_size:
      return f"Error: File is too large ({size} bytes)"
    
    with open(path,"r" , encoding="utf-8",errors="replace") as f:
      return f.read()
  
  except PermissionError:
    return "Error: Permission denied"
  
  except Exception as e:
    return f"Error reading file : {str(e)}"
    
    
