import os
from typing_extensions import Tuple

from config import MAX_CHARS


def get_file_content(working_directory: str, file_path: str) -> str:
    target_file, err = check_path(working_directory, file_path)
    if not target_file:
        return err
    try:
        with open(target_file, "r") as f:
            content = f.read(MAX_CHARS)
            # After reading the first MAX_CHARS...
            if f.read(1):
                content += f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'
        return content
    except Exception as e:
        return f'Error: {e}'

def check_path(working_directory: str, file_path: str = ".") -> Tuple[str | None, str]:
    try:
        abs_working_dir = os.path.abspath(working_directory)
        target_file:str = os.path.normpath(os.path.join(abs_working_dir, file_path))
        valid_target_file = os.path.commonpath([abs_working_dir, target_file]) == abs_working_dir
        if not valid_target_file:
            return None, f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        if not os.path.isfile(target_file):
            return None, f'Error: File not found or is not a regular file: "{file_path}"'
        return target_file, ""
    except Exception as e:
        return None, f'Error: {e}'
