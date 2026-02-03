import ast

def ast_func(src_code: str , fun_name:str):
  try:
    par = ast.parse(src_code) ## parse the code
  
  except SyntaxError as e:
    raise ValueError(f"Invalid python syntax {e}") 
  
  for node in ast.walk(par):
    if isinstance(node,ast.FunctionDef) and node.name == fun_name:
      if not hasattr(node,"end_lineno"):
        raise ValueError("error in code")
      
      return node.lineno , node.end_lineno
    
  raise ValueError(f"Function {fun_name}  not found")  

# code = """
# def add(a, b):
#     return a + b

# testing = "abc"
# """

# print(ast_func(code, "add"))

