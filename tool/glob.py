import os
import glob

max_matches = 100

def glob_files(pattern: str) -> str:

  if not pattern:
    return "Error: search is not provided"
  
  try:
    matches = glob.glob(pattern,recursive=True)

    if not matches:
      return "No files found"
    
    matches = matches[:max_matches] ## slice the lis to 0 to 100(max_result)

    return "\n".join(matches)
  
  except Exception as e:
    return f"Error finding files {str(e)}"
  