def confirmChanges(diff_txt:str):
  print("\n here are the changes which are done by agent")
  print(diff_txt)
  print("\n do you want to apply these changes")
  user_input = input("Type Yes to confirm :" ).strip().lower()

  return user_input == "yes"