# Executing the Python script: python src/main.py

# Import required libraries for automation, logging, and time management
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import time
import logging
import os

# Configure logging to capture key events and errors
logging.basicConfig(filename='process.log', level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Check if the specified file exists before processing
def check_file_existence(file_path):
    try:
        with open(file_path) as f:
            logging.info(f"File {file_path} exists.")
            return True
    except FileNotFoundError:
        logging.error(f"File {file_path} not found.")
        return False

# Load keywords from the provided CSV file and handle encoding errors
def load_keywords(file_path):
    if check_file_existence(file_path):
        try:
            # Add encoding parameter to handle non-UTF-8 encoded files
            df = pd.read_csv(file_path, encoding='ISO-8859-1')  # Try ISO-8859-1 or another encoding
            logging.info(f"Loaded {len(df)} keywords from {file_path}.")
            return df
        except pd.errors.EmptyDataError:
            logging.error(f"File {file_path} is empty.")
        except pd.errors.ParserError:
            logging.error(f"File {file_path} has parsing errors.")
        except UnicodeDecodeError as e:
            logging.error(f"Encoding error in file {file_path}: {e}")
    return None

# Initialize the Chrome WebDriver for automation tasks
def setup_driver(chrome_driver_path):
    try:
        service = Service(chrome_driver_path)
        driver = webdriver.Chrome(service=service)
        logging.info("WebDriver initialized successfully.")
        return driver
    except Exception as e:
        logging.error(f"Failed to initialize WebDriver: {e}")
        return None

# Open Google in the current browser tab
def open_google(driver):
    try:
        driver.get("http://www.google.com")
        time.sleep(2)  # Allow page to fully load
        logging.info("Google page opened.")
    except Exception as e:
        logging.error(f"Failed to open Google: {e}")

# Locate Google's search box
def find_search_box(driver):
    try:
        return driver.find_element(By.NAME, "q")
    except Exception as e:
        logging.error(f"Search box not found: {e}")
        return None

# Perform a search with the provided keyword
def enter_keyword_and_search(search_box, keyword):
    try:
        search_box.send_keys(keyword)
        search_box.send_keys(Keys.RETURN)
        logging.info(f"Search executed for keyword: {keyword}")
    except Exception as e:
        logging.error(f"Error during search for keyword '{keyword}': {e}")

# Perform a full search sequence on Google for a keyword
def search_keyword_on_google(driver, keyword):
    open_google(driver)
    search_box = find_search_box(driver)
    if search_box:
        enter_keyword_and_search(search_box, keyword)

# Open a new browser tab and switch focus to it
def open_and_switch_to_new_tab(driver):
    try:
        driver.execute_script("window.open('');")
        driver.switch_to.window(driver.window_handles[-1])
        logging.info("Switched to new tab.")
    except Exception as e:
        logging.error(f"Failed to open or switch to new tab: {e}")

# Close a specific tab based on its index
def close_tab(driver, tab_index):
    try:
        driver.switch_to.window(driver.window_handles[tab_index])
        driver.close()
        logging.info(f"Closed tab {tab_index}.")
    except Exception as e:
        logging.error(f"Error closing tab {tab_index}: {e}")

# Close all tabs except the first one
def close_all_extra_tabs(driver):
    while len(driver.window_handles) > 1:
        close_tab(driver, -1)
    try:
        driver.switch_to.window(driver.window_handles[0])
        logging.info("Returned to the first tab.")
    except Exception as e:
        logging.error(f"Error switching to the first tab: {e}")

# Process a batch of keywords, performing searches and opening new tabs for each
def process_keywords_in_batches(df, driver, batch_size=15, start_index=0):
    counter = start_index

    for keyword in df['Keyword'][start_index:]:
        if pd.isna(keyword):  # Stop if a keyword is missing
            logging.info("Empty keyword found. Stopping batch.")
            break
        
        open_and_switch_to_new_tab(driver)
        search_keyword_on_google(driver, keyword)
        time.sleep(1)  # Pause briefly between searches
        
        counter += 1
        
        if counter % batch_size == 0:
            logging.info(f"Batch of {batch_size} completed. Pausing.")
            save_progress(counter)
            return  # End the batch without closing the browser

    logging.info("All keywords processed.")

# Save the progress of keyword processing to a file for later resumption
def save_progress(counter):
    with open('progress.txt', 'w') as f:
        f.write(str(counter))
    logging.info(f"Progress saved at keyword {counter}.")

# Load the progress from a file to resume keyword processing
def load_progress():
    if os.path.exists('progress.txt'):
        with open('progress.txt', 'r') as f:
            return int(f.read())
    return 0  # Default to starting from the first keyword

# Main execution logic: load data, set up the driver, and process keywords
if __name__ == "__main__":
    file_path = '/Users/chaeyeonkim/Projects/Python_Project/data/Instagram_Keyword.csv'
    df = load_keywords(file_path)

    if df is not None:
        chrome_driver_path = '/Users/chaeyeonkim/Downloads/chromedriver-mac-x64/chromedriver'
        driver = setup_driver(chrome_driver_path)

        if driver is not None:
            start_index = load_progress()
            process_keywords_in_batches(df, driver, batch_size=15, start_index=start_index)

            logging.info("Keeping browser open for manual tasks.")
            time.sleep(600)  # Pause execution for 10 minutes before closing manually
