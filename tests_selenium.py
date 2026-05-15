# /// script
# dependencies = [
#   "selenium",
# ]
# ///

import os
import time
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Colores para la terminal
GREEN = "\033[92m"
RED = "\033[91m"
BLUE = "\033[94m"
BOLD = "\033[1m"
RESET = "\033[0m"

BASE_URL = "http://127.0.0.1:8000"
TEST_USER = "admin"
TEST_PASS = "admin"

HEADLESS = False  
#HEADLESS = True  

def print_status(step, passed):
    status = f"{GREEN}✔ PASSED{RESET}" if passed else f"{RED}✘ FAILED{RESET}"
    print(f"{BOLD}{step:<25}{RESET} {status}")

def run_test():
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    project_title = f"Test: {timestamp}"
    file_path = os.path.abspath("test_upload_file.txt")
    
    if not os.path.exists(file_path):
        with open(file_path, "w") as f: f.write("test content")

    opts = Options()
    opts.add_argument("--window-size=1600,1000")
    
    if HEADLESS:
        opts.add_argument("--headless")
    
    driver = webdriver.Chrome(options=opts)
    wait = WebDriverWait(driver, 10)

    print(f"\n{BLUE}{BOLD} INICIANDO TEST{RESET}")
    print("-" * 35)

    try:
        # 1. Login
        driver.get(f"{BASE_URL}/accounts/login/")
        wait.until(EC.presence_of_element_located((By.NAME, "username"))).send_keys(TEST_USER)
        driver.find_element(By.NAME, "password").send_keys(TEST_PASS + Keys.ENTER)
        wait.until(EC.presence_of_element_located((By.XPATH, "//button[contains(text(), 'Logout')]")))
        print_status("User Login", True)

        # 2. Create Project
        driver.get(f"{BASE_URL}/project/new/")
        title_field = wait.until(EC.presence_of_element_located((By.NAME, "title")))
        title_field.send_keys(project_title)
        driver.find_element(By.NAME, "description").send_keys("Automated test")
        
        # Archivo
        driver.find_element(By.ID, "fileInput").send_keys(file_path)
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, "new-file-badge")))
        
        title_field.send_keys(Keys.ENTER)
        time.sleep(2)
        print_status("Project Create", True)

        # 3. Verify Project
        driver.get(f"{BASE_URL}/")
        v_xpath = f"//h5[contains(@class, 'card-title') and contains(text(), '{timestamp}')]"
        wait.until(EC.presence_of_element_located((By.XPATH, v_xpath)))
        print_status("Successfully created", True)
        
        # Prient project name and file name
        
        project_card = driver.find_element(By.XPATH, v_xpath)
        print(f"\n{BOLD}Project Name:{RESET} {project_card.text}")

        print("-" * 35)
        print(f"{GREEN}{BOLD} TEST COMPLETADO {RESET}\n")

    except Exception as e:
        print("-" * 35)
        print(f"{RED}{BOLD} TEST FALLIDO {RESET}")
        print(f"Detail: {e}")
    
    finally:
        driver.quit()

if __name__ == "__main__":
    run_test()