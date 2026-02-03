import os

def list_files(directory="."): #  . means current 
  try:
    all_items = os.listdir(directory)

    non_sensitive_items = []

    for items in all_items:
      if not items.startswith('.'):
        non_sensitive_items.append(items)

    if non_sensitive_items:
      return "\n".join(non_sensitive_items)
    
    else:
      return "Directory is empty"
  
  except Exception as e:
    return "Error reading directory" + str(e)

    

