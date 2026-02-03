from tool import grep
from tool.edit_file import edit
from tool.execute_cmd import exe_cmd
from tool.glob import glob_files
from tool.tool_manager import ToolManager
from tool.list_file import list_files
from tool.read import read_file
from tool.webSearch_tool import webSearch
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

tool_manager.register(
    name="execute_command",
    description="Execute a terminal command (like 'python file.py'). captures output and errors.",
    parameters={
        "type": "object",
        "properties": {
            "command": {
                "type": "string",
                "description": "The command to run in the terminal"
            }
        },
        "required": ["command"]
    },
    tool=exe_cmd
)

tool_manager.register(
    name="glob",
    description="Find files using a pattern (like *.py or **/*.md)",
    parameters={
        "type": "object",
        "properties": {
            "pattern": {
                "type": "string",
                "description": "Glob pattern to search files"
            }
        },
        "required": ["pattern"]
    },
    tool=glob_files
)

tool_manager.register(
    name="grep",
    description="Search text inside a file",
    parameters={
        "type": "object",
        "properties": {
            "path": {
                "type": "string",
                "description": "File path"
            },
            "text": {
                "type": "string",
                "description": "Text to search"
            }
        },
        "required": ["path", "text"]
    },
    tool=grep.grep
)

tool_manager.register(
    name="webSearch",
    description="Search the web for up-to-date information",
    parameters={
        "type": "object",
        "properties": {
            "query": {
                "type": "string",
                "description": "Search query"
            }
        },
        "required": ["query"]
    },
    tool=webSearch
)

