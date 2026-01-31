import os

max_file_size = 200 * 1024

def normalize_line(line):
 return line.strip()

def edit(path:str,search:str,replace:str) -> str:

  try:

    if not path or ".." in path:
     return "Error: Invalid file path"
  
    if not os.path.exists(path):
     return "Error: File not found"
  
    if not os.path.isfile(path):
     return "Error:file is not valid"
  
    if not search:
     return "Error:search text not provided"
  
    if os.path.getsize(path) > max_file_size:
     return "Error: file is too large"
  
    ## read file and get the content
  
    with open(path,"r",encoding="utf-8",errors="replace") as f:
     content = f.read()

    # simple case extract match and replace

    if search in content:
     new_content = content.replace(search,replace,1)
     return new_content
  
    content_lines = content.splitlines(keepends=True)

    ## so this what this do ex
    ## hello
    ## world
    ## result ['hello\n','world\n']

    search_lines = search.splitlines(keepends=False) ## false means no \n in end

    clean_lines = []

    for line in search_lines:
     if line.strip(): ## line is not empty
      clean_lines.append(line)

    search_lines = clean_lines

    if not search_lines:
     return "Error: Search only contains empty line"
    
    matched_index = None

    normlize_search = [normalize_line(line) for line in search_lines]

    for i  in range(len(content_lines) - len(search_lines)+1):
     
      chunk = content_lines[i: i + len(search_lines)]

      norm_chunk = [normalize_line(line) for line in chunk]

      if norm_chunk == normlize_search:
       matched_index = i
       break
    
    if matched_index != None:
     new_content_line = content_lines[:matched_index]

     if replace and not replace.endswith('\n') and matched_index + len(search_lines) < len(content_lines):
        replace += '\n'
     
     new_content_line.append(replace)

     new_content_line.extend(content_lines[matched_index + len(search_lines):])

     new_content = "".join(new_content_line)
     return new_content
    
    return "Error: Content not found. The tool could not locate the code to replace. Please read the file first to ensure exact matching."
  
  except Exception as e:
        return f"Error editing file: {str(e)}"

  
## our privous code is just simple content match

# def edit(path:str,search:str,replace:str) -> str:
#   try:
#     if not path and ".." in path:
#       return "Error: invalid file path"
    
#     if not os.path.exists(path):
#       return "Error: File not found"
    
#     if not os.path.isfile(path):
#       return "Error: path is not file"
    
#     if not search:
#       return "Error: search text not provided"
    
#     if os.path.getsize(path) > max_file_size:
#       return "Error: file too large"
    
#     ## read file

#     with open(path,'r',encoding="utf-8",errors="replace") as f:
#       content = f.read()
    
#     if search not in content:
#       return "Error content not find in file"
    
#     ## so we are going to replace the first occurance for just safety pupose

#     new_content = content.replace(search,replace,1)

#     if content == new_content:
#       return "No changes made"
    
#     return new_content
    
#   except Exception as e:
#     return f"Error edditing file {str(e)}"