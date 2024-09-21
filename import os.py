import os
import subprocess

# Define project paths
project_root = os.path.expanduser('~/Projects/Python_Project')
venv_path = os.path.join(project_root, 'venv')
data_path = os.path.join(project_root, 'data')
src_path = os.path.join(project_root, 'src')
main_file_path = os.path.join(src_path, 'main.py')
requirements_path = os.path.join(project_root, 'requirements.txt')
readme_path = os.path.join(project_root, 'README.md')

# Step 1: Create the folder structure
def create_folder_structure():
    try:
        # Create project directories
        os.makedirs(venv_path, exist_ok=True)
        os.makedirs(data_path, exist_ok=True)
        os.makedirs(src_path, exist_ok=True)
        print("Project directories created successfully.")
    except Exception as e:
        print(f"Error creating directories: {e}")

# Step 2: Set up the virtual environment
def setup_virtual_environment():
    try:
        # Create virtual environment
        subprocess.run(['python3', '-m', 'venv', venv_path], check=True)
        print("Virtual environment created successfully.")
    except Exception as e:
        print(f"Error creating virtual environment: {e}")

# Step 3: Create placeholder files
def create_placeholder_files():
    try:
        # Create main.py
        with open(main_file_path, 'w') as f:
            f.write("# Your main Python script\n")
            f.write("# You can move your existing code here\n")
        
        # Create requirements.txt
        with open(requirements_path, 'w') as f:
            f.write("# List of required packages\n")

        # Create README.md
        with open(readme_path, 'w') as f:
            f.write("# Project Documentation\n")
            f.write("This is an optional README file.\n")
        
        print("Placeholder files created successfully.")
    except Exception as e:
        print(f"Error creating files: {e}")

# Step 4: Add your existing Python code to main.py
def add_existing_code_to_main():
    try:
        code = """
# Step 1: Import required libraries
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

# Step 2: Load the keywords from the CSV file
def check_file_existence(file_path):
    try:
        with open(file_path) as f:
            print(f"File {file_path} exists.")
            return True
    except FileNotFoundError:
        print(f"File {file_path} not found.")
        return False

def load_keywords(file_path):
    if check_file_existence(file_path):
        try:
            df = pd.read_csv(file_path)
            print(f"Successfully loaded {len(df)} keywords.")
            return df
        except pd.errors.EmptyDataError:
            print(f"File {file_path} is empty.")
            return None
        except pd.errors.ParserError:
            print(f"File {file_path} has parsing errors.")
            return None
    return None

# Example usage:
file_path = '/Users/chaeyeonkim/Library/CloudStorage/OneDrive-Personal/Chartmetric/Instagram_Keyword.csv'
df = load_keywords(file_path)
"""
        # Write the existing code into main.py
        with open(main_file_path, 'a') as f:
            f.write(code)
        
        print("Existing code added to main.py successfully.")
    except Exception as e:
        print(f"Error adding existing code to main.py: {e}")

# Execute all steps
if __name__ == "__main__":
    create_folder_structure()
    setup_virtual_environment()
    create_placeholder_files()
    add_existing_code_to_main()
