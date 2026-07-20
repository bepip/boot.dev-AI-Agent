from config import MAX_CHARS
from functions.get_file_content import get_file_content

def main():
    run_test("calculator", "lorem.txt")
    run_test("calculator", "main.py")
    run_test("calculator", "pkg/calculator.py")
    run_test("calculator", "/bin/cat")
    run_test("calculator", "pkg/does_not_exist.py")

def run_test(working_directory:str, file_path:str):
    print(f"running test with input: working_directory={working_directory}, file_path={file_path}")
    result = get_file_content(working_directory, file_path)
    print(f"{file_path} length: {len(result)}")
    print(f"{file_path} truncated: {'truncated' in result}")
    if len(result) < MAX_CHARS:
        print(result)


if __name__ == "__main__":
    main()
