from tool.tool_manager import ToolManager
from tool.list_file import list_files
from tool.read import read_file

tool_manager = ToolManager()

# list_files
tool_manager.register(
    name="list_files",
    description="List files in a directory",
    parameters={
        "type": "object",
        "properties": {
            "directory": {
                "type": "string",
                "description": "Directory path",
                "default": "."
            }
        }
    },
    tool=list_files
)

# read_file
tool_manager.register(
    name="read_file",
    description="Read the contents of a text file",
    parameters={
        "type": "object",
        "properties": {
            "path": {
                "type": "string",
                "description": "Relative path to the file"
            }
        },
        "required": ["path"]
    },
    tool=read_file
)