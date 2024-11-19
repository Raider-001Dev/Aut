import os
import time
import json
import logging
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# Logging setup
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

TOKEN_FILE = "token.txt"

# Scrape proxy with error handling
def scrape_proxy():
    url = "https://www.sslproxies.org/"
    try:
        response = requests.get(url, timeout=10)
        proxies = []
        if response.status_code == 200:
            from bs4 import BeautifulSoup
            soup = BeautifulSoup(response.text, "html.parser")
            rows = soup.find_all("tr")
            for row in rows:
                columns = row.find_all("td")
                if len(columns) > 1:
                    proxies.append(f"{columns[0].text}:{columns[1].text}")
        return proxies[:5]
    except Exception as e:
        logging.error(f"Failed to scrape proxies: {e}")
        return []

# Configure Selenium WebDriver
def configure_driver():
    chrome_options = Options()
    chrome_options.add_argument("--incognito")
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("disable-blink-features=AutomationControlled")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--no-sandbox")
    
    proxies = scrape_proxy()
    if proxies:
        proxy = proxies[0]
        chrome_options.add_argument(f"--proxy-server={proxy}")
        logging.info(f"Using Proxy: {proxy}")
    return webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

# GitHub Login with validation
def github_login(driver, username, password):
    logging.info("Opening GitHub login page...")
    driver.get("https://github.com/login")
    try:
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "login_field"))).send_keys(username)
        driver.find_element(By.ID, "password").send_keys(password)
        driver.find_element(By.NAME, "commit").click()
        time.sleep(2)  # Allow time for page to load
        if "incorrect" in driver.page_source.lower():
            logging.error("Login failed: Incorrect username or password")
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

# Monitor Codespace with retry mechanism
def monitor_codespace(driver):
    while True:
        try:
            driver.refresh()
            if "stopped" in driver.page_source.lower():
                logging.warning("Codespace stopped! Restarting...")
                driver.find_element(By.XPATH, "//button[contains(text(), 'Restart')]").click()
                time.sleep(10)
            else:
                logging.info("Codespace is running...")
            time.sleep(30)
        except Exception as e:
            logging.error(f"Error monitoring Codespace: {e}")
            time.sleep(5)

def main():
    driver = configure_driver()
    username = input("Enter GitHub username: ")
    password = input("Enter GitHub password: ")
    if github_login(driver, username, password):
        generate_token(driver)
        monitor_codespace(driver)
    else:
        logging.error("Login failed. Exiting program.")

if __name__ == "__main__":
    main()
