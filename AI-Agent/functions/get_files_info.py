import os
from typing_extensions import Tuple

schema_get_files_info = {
    "type": "function",
    "function": {
        "name": "get_files_info",
        "description": "Lists files in a specified directory relative to the working directory, providing file size and directory status",
        "parameters": {
            "type": "object",
            "properties": {
                "directory": {
                    "type": "string",
                    "description": "Directory path to list files from, relative to the working directory (default is the working directory itself)",
                },
            },
        },
    },
}

def get_files_info(working_directory: str, directory: str = ".") -> str:
    target_dir, err = check_path(working_directory, directory)
    if not target_dir:
        return err
    try:
        contents = os.listdir(target_dir)
        files_infos: str = ""
        for file in contents:
            target_path = os.path.join(target_dir, file)
            files_infos += f"- {file}: file_size={os.path.getsize(target_path)}, is_dir={os.path.isdir(target_path)}\n"
        return files_infos
    except Exception as e:
        return f'Error: {e}'

def check_path(working_directory: str, directory: str = ".") -> Tuple[str | None, str]:
    try:
        abs_working_dir = os.path.abspath(working_directory)
        target_dir:str = os.path.normpath(os.path.join(abs_working_dir, directory))
        valid_target_dir = os.path.commonpath([abs_working_dir, target_dir]) == abs_working_dir
        if not valid_target_dir:
            return None, f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
        if not os.path.isdir(target_dir):
            return None, f'Error: "{directory}" is not a directory'
        return target_dir, ""
    except Exception as e:
        return None, f'Error: {e}'

