from tool.edit_file import edit
from tool.tool_manager import ToolManager
from tool.list_file import list_files
from tool.read import read_file
from tool.write import writeFile

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

# write

tool_manager.register(
  name="write_file",
    description="Create or update a text file",
    parameters={
        "type": "object",
        "properties": {
            "path": {
                "type": "string",
                "description": "Relative path to the file"
            },
            "content": {
                "type": "string",
                "description": "Text content to write"
            },
            "mode": {
                "type": "string",
                "enum": ["overwrite", "append"],
                "description": "Write mode"
            }
        },
        "required": ["path", "content", "mode"]
    },
    tool=writeFile
)

tool_manager.register(
    name="edit_file",
    description="Edit a specific part of a file using search and replace",
    parameters={
        "type": "object",
        "properties": {
            "path": {
                "type": "string",
                "description": "Relative path to the file"
            },
            "search": {
                "type": "string",
                "description": "Text to search for"
            },
            "replace": {
                "type": "string",
                "description": "Replacement text"
            }
        },
        "required": ["path", "search", "replace"]
    },
    tool=edit
)
