import os
import shutil

def create_folders_and_files(directory):
    # Get the directory name
    folder_name = 'pygbag_builder_build'

    # Create the path for the folder
    new_folder_path = os.path.join(directory, folder_name)

    # If the folder already exists, delete it
    if os.path.exists(new_folder_path):
        shutil.rmtree(new_folder_path)

    # Create a folder under the current directory (If the folder already exists, do nothing.)
    os.makedirs(new_folder_path, exist_ok=True)

    # Create '.github/workflows' folder 
    github_workflows_path = os.path.join(new_folder_path, '.github', 'workflows')
    os.makedirs(github_workflows_path, exist_ok=True)

    # The content of pygbag.yml
    yml_content = """name: Build and Deploy Pygbag

on:
  push:
    branches:
      - main

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v3

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.10'

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install pygbag

      - name: Build with pygbag
        run: |
          pygbag build
"""

    # Create the path for pygbag.yml (.github/workflows/pygbag.yml)
    yml_file_path = os.path.join(github_workflows_path, 'pygbag.yml')

    # Create pygbag.yml in .github/workflows
    with open(yml_file_path, 'w', encoding='utf-8') as f:
        f.write(yml_content)

    # Copy files and folders from the current directory to the new folder, excluding .py files, __pycache__ folders, and the new folder itself
    for item in os.listdir(directory):
        s = os.path.join(directory, item)
        d = os.path.join(new_folder_path, item)
        if item == folder_name:
            continue
        if os.path.isdir(s):
            if item != '__pycache__':
                shutil.copytree(s, d, ignore=shutil.ignore_patterns('*.py', '__pycache__'))
        else:
            if not item.endswith('.py'):
                shutil.copy2(s, d)
        
    print(f"'{new_folder_path}' and '.github/workflows/pygbag.yml' have been successfully created.")

if __name__ == "__main__":
    current_directory = os.getcwd()
    create_folders_and_files(current_directory)