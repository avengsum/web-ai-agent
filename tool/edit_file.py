import os

max_file_size = 200 * 1024

def edit(path:str,search:str,replace:str) -> str:
  try:
    if not path and ".." in path:
      return "Error: invalid file path"
    
    if not os.path.exists(path):
      return "Error: File not found"
    
    if not os.path.isfile(path):
      return "Error: path is not file"
    
    if not search:
      return "Error: search text not provided"
    
    if os.path.getsize(path) > max_file_size:
      return "Error: file too large"
    
    ## read file

    with open(path,'r',encoding="utf-8",errors="replace") as f:
      content = f.read()
    
    if search not in content:
      return "Error content not find in file"
    
    ## so we are going to replace the first occurance for just safety pupose

    new_content = content.replace(search,replace,1)

    if content == new_content:
      return "No changes made"
    
  except Exception as e:
    return f"Error edditing file {str(e)}"