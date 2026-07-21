import os
from typing import Tuple
import subprocess


schema_run_python_file = {
    "type": "function",
    "function": {
        "name": "run_python_file",
        "description": "Execute python file (only accepts *.py extensions). The given file name is relative to the working directory",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "File path to execute from, relative to the working directory",
                },
                "args": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Optional list of arguments to pass to the Python script",
                    }
            },
            "required": ["file_path"],
        },
    },
}

def run_python_file(
        working_directory: str, file_path: str, args: list[str] | None = None
        ) -> str:
    target_file, err = check_path(working_directory, file_path)
    if not target_file:
        return err
    try:
        command = ["python", target_file]
        if args:
            command.extend(args)
        process = subprocess.run(command,
                                 text = True,
                                 capture_output= True,
                                 cwd=os.path.dirname(target_file),
                                 timeout=30
                                 )
        output_str = ""
        if process.returncode != 0:
            output_str += f'Process exited with code {process.returncode}\n'
        if not process.stdout and not process.stderr:
            output_str += f'No output produced\n'
        if process.stdout:
            output_str += f'STDOUT: {process.stdout}\n'
        if process.stderr:
            output_str += f'STDERR: {process.stderr}'
        return output_str
    except Exception as e:
        return f'Error: {e}'


def check_path(working_directory: str, file_path: str = ".") -> Tuple[str | None, str]:
    try:
        abs_working_dir = os.path.abspath(working_directory)
        target_file:str = os.path.normpath(os.path.join(abs_working_dir, file_path))
        valid_target_file = os.path.commonpath([abs_working_dir, target_file]) == abs_working_dir
        if not valid_target_file:
            return None, f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        if not os.path.isfile(target_file):
            return None, f'Error: "{file_path}" does not exist or is not a regular file'
        if not target_file.endswith(".py"):
            return None, f'Error: "{file_path}" is not a Python file'
        return target_file, ""
    except Exception as e:
        return None, f'Error: {e}'
