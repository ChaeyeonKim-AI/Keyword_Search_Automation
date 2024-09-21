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
file_path = '/Users/chaeyeonkim/Projects/Python_Project/data/Instagram_Keyword.csv'
df = load_keywords(file_path)

# Check if data is loaded correctly
if df is not None:
    print(df.head())
else:
    print("No data loaded.")
