import subprocess
import os

timeout = 10 ## this is default timeout

not_allow = ["rm -rf" , "sudo","shutdown","reboot"]


def exe_cmd(command: str) -> str:

  try:
    if any(bad in command for bad in not_allow):
      return "Error: this cmd is not allow"
    
    print(f"Running: {command}")

    result = subprocess.run(
      command,
      shell=True,
      capture_output=True,
      text=True,
      cwd=os.getcwd(),
      timeout=timeout
    )

    ## ok this result will be printed

    output = result.stdout

    if result.stderr:
      output += f"\n[Stderr]:\n{result.stderr}"
    
    if not output.strip():
      return "Cmd execute no output"
    
    return output
  
  except subprocess.TimeoutExpired:
    return f"Error: command timed out after {timeout}"
  
  except Exception as e:
    return f"Error executin command: {str(e)}"
