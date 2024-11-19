import os
import time
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import random

# Logging setup
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

TOKEN_FILE = "token.txt"

# List of random User-Agents
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.5672.63 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.5615.49 Safari/537.36",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/109.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edge/113.0.1774.35",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.4 Safari/605.1.15"
]

# Configure Selenium WebDriver with randomized User-Agent
def configure_driver():
    chrome_options = Options()
    chrome_options.add_argument("--incognito")
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--headless=new")  # Optional for headless mode
    chrome_options.add_argument(f"user-agent={random.choice(USER_AGENTS)}")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    try:
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
        logging.info("Chrome WebDriver successfully configured and launched.")
        return driver
    except Exception as e:
        logging.error(f"Failed to configure WebDriver: {e}")
        raise SystemExit("Exiting due to WebDriver initialization failure.")

# GitHub Login with validation
def github_login(driver, username, password):
    logging.info("Opening GitHub login page...")
    driver.get("https://github.com/login")
    try:
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "login_field"))).send_keys(username)
        driver.find_element(By.ID, "password").send_keys(password)
        driver.find_element(By.NAME, "commit").click()

        # Check for OTP prompt
        if "two-factor" in driver.page_source.lower():
            logging.info("OTP required. Prompting user for input...")
            otp_code = input("Enter OTP code: ")
            otp_input = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "otp")))
            otp_input.send_keys(otp_code)
            otp_input.send_keys(Keys.RETURN)
            time.sleep(2)

        # Check for errors
        if "incorrect" in driver.page_source.lower():
            logging.error("Login failed: Incorrect username, password, or OTP.")
            return False
        if "suspended" in driver.page_source.lower():
            logging.error("Account suspended or banned.")
            return False

        logging.info("Successfully logged in!")
        return True
    except Exception as e:
        logging.error(f"Error during login: {e}")
        return False

# Generate and save token
def generate_token(driver):
    logging.info("Generating GitHub token...")
    driver.get("https://github.com/settings/tokens/new")
    try:
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "token_description"))).send_keys("Automated Token")
        driver.find_element(By.XPATH, "//input[@value='repo']").click()
        driver.find_element(By.XPATH, "//button[contains(text(), 'Generate token')]").click()
        token = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//code"))).text
        with open(TOKEN_FILE, "a") as f:
            f.write(f"{token}\n")
        logging.info(f"Token saved: {token}")
    except Exception as e:
        logging.error(f"Error generating token: {e}")

# Open Codespace and execute command
def open_codespace_and_execute(driver):
    logging.info("Opening GitHub Codespace...")
    driver.get("https://github.com/codespaces")
    try:
        codespace = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//a[contains(@href, '/codespaces/')]")))
        codespace.click()
        time.sleep(5)  # Wait for Codespace to load

        # Prompt user for terminal command
        command = input("Enter the command you want to run in the terminal: ")
        logging.info(f"Executing command: {command}")
        terminal_input = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//textarea[@data-testid='terminal-input']")))
        terminal_input.send_keys(command + Keys.RETURN)
        logging.info("Command executed successfully.")
    except Exception as e:
        logging.error(f"Error opening Codespace or executing command: {e}")

# Monitor opened tabs in layout (1 row, 5 tabs)
def monitor_tabs(driver):
    logging.info("Setting up monitoring layout...")
    for i in range(5):
        driver.execute_script("window.open('https://github.com/codespaces', '_blank');")
    windows = driver.window_handles
    for i, window in enumerate(windows):
        driver.switch_to.window(window)
        driver.set_window_rect(0 + i * 200, 0, 800, 600)  # Adjust layout

    logging.info("Monitoring tabs initialized. Active tabs:")
    for i, window in enumerate(windows):
        driver.switch_to.window(window)
        logging.info(f"Tab {i+1}: {driver.current_url}")

def main():
    while True:
        choice = input("Do you want to add a new account or go to monitoring? (new/monitor): ").strip().lower()
        if choice == "new":
            driver = configure_driver()
            username = input("Enter GitHub username: ")
            password = input("Enter GitHub password: ")

            if github_login(driver, username, password):
                generate_token(driver)
                open_codespace_and_execute(driver)

        elif choice == "monitor":
            driver = configure_driver()
            monitor_tabs(driver)
            break

        else:
            logging.warning("Invalid choice. Please select 'new' or 'monitor'.")

if __name__ == "__main__":
    main()
