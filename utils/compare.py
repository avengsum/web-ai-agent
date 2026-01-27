import difflib

def compare(old:str,new:str,path:str) -> str:
  old_lines = old.splitlines(keepends=True)
  ## splitlines do this example hello\nworld\n -> [hello\n , world\n]

  new_lines = new.splitlines(keepends=True)

  difference = difflib.unified_diff(old_lines,new_lines,fromfile=path,tofile=path,lineterm="") 
  ## from file aur to file sirf label ke liye h ki konsa file h jisme changes hue h

  diff_text = "".join(difference)

  if not diff_text.strip():
    return "No changes"
  
  return diff_text