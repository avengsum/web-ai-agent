import json


class ToolManager:
  def __init__(self):
    self._tools = {}
    self._schema = []

  def register(self,*,name,description,parameters,tool): ## idhar * position ke liye 

    ## save fucntion
    self._tools[name] = tool

    ## save schema for llm

    self._schema.append({
      "type":"function",
      "function":{
        "name":name,
        "description":description,
        "parameters":parameters
      }
    })

  
  def getSchema(self):
    return self._schema
  
  def run(self,tool_call):
    ## this will run the tool which is called by llm and return will be in string always

    name = tool_call["function"]["name"]
    agrument = tool_call["function"].get("arguments","")

    if name not in self._tools:
      return f"Error unkown tool {name}"
    
    try:
      args = json.loads(agrument) if agrument else {}

      if args is None:
        args = {}

    except json.decoder.JSONDecodeError:
      return "Error: invalid json argument from llm"
    
    try:
      return self._tools[name](**args)
    
    except TypeError as e:
      return f"Error: Tool arguments mismatch. {str(e)}"
    
    ## ** used because llm give you this data {path : main.py }
    ## so direct ye pass karoge to error confirm h so ** isko main.py kar deta h simple
    
    except Exception as e:
      return f"Error: executing tool {name} {str(e)}"
  
    



