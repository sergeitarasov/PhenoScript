import os


def my_function():
    module_path = os.path.dirname(__file__)
    file_path = os.path.join(module_path, "myfile.txt")
    print(file_path)
