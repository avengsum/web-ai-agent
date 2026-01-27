tools = [
    {
        "type": "function",
        "function": {
            "name": "list_files",
            "description": "List files in a directory",
            "parameters": {
                "type": "object",
                "properties": {
                    "directory": {
                        "type": "string",
                        "description": "Directory path",
                        "default": "."
                    }
                },
                "required": []
            }
        }
    },
    {
    "type": "function",
    "function": {
        "name": "read_file",
        "description": "Read the contents of a text file",
        "parameters": {
            "type": "object",
            "properties": {
                "path": {
                    "type": "string",
                    "description": "Relative path to the file to read"
                }
            },
            "required": ["path"]
        }
      }
   }

]