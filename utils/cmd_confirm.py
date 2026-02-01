def cmdConfirm(cmd:str):
  print(f"\n this is the {cmd} agent want to run")
  print(cmd)
  print("\n do you want the agent to the run the cmd")
  user_input = input("Type Yes to confirm :" ).strip().lower()

  return user_input == "yes"