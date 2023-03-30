import inspect
import os

# Set the directory containing the Python files
dir_path ='/Users/taravser/Documents/My_papers/PhenoScript_main/PhenoScript/phenospy_package/phenospy'

# Loop over the files in the directory
for file_name in os.listdir(dir_path):
    # Check if the file is a Python file
    if file_name.endswith('.py'):
        # Get the full path to the file
        file_path = os.path.join(dir_path, file_name)

        # Get the source code of the file
        with open(file_path, 'r') as f:
            source = f.read()

        # Find all function definitions in the source code
        functions = [line.strip() for line in source.split('\n') if line.startswith('def ')]

        # Print the list of functions
        print(f'Functions in {file_name}: {functions}')