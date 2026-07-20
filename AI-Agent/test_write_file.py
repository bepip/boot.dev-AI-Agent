from functions.write_file import write_file

def main():
    run_test("calculator", "lorem.txt", "wait, this isn't lorem ipsum")
    run_test("calculator", "pkg/morelorem.txt", "lorem ipsum dolor sit amet")
    run_test("calculator", "/tmp/temp.txt", "this should not be allowed")

def run_test(working_directory:str, file_path:str, content: str):
    print("============================================")
    print(f"running test with input: working_directory={working_directory}, file_path={file_path}")

    result =  write_file(working_directory, file_path, content)
    print(result)
    print("============================================")


if __name__ == "__main__":
    main()
