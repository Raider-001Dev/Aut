import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

def setup_driver(proxy=None):
    # Konfigurasi ChromeDriver dengan opsi tambahan
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Jalankan tanpa GUI
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.binary_location = "/usr/bin/chromium-browser"  # Path untuk Chromium

    if proxy:
        chrome_options.add_argument(f"--proxy-server={proxy}")

    # Inisialisasi ChromeDriver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    return driver

def login_to_github(driver, username, password):
    driver.get("https://github.com/login")
    time.sleep(2)

    # Input username
    driver.find_element(By.ID, "login_field").send_keys(username)
    # Input password
    driver.find_element(By.ID, "password").send_keys(password)
    driver.find_element(By.NAME, "commit").click()

    time.sleep(3)

    # Cek jika OTP diperlukan
    if "two-factor" in driver.current_url:
        otp = input("Masukkan kode OTP yang diterima: ")
        driver.find_element(By.ID, "otp").send_keys(otp)
        driver.find_element(By.XPATH, "//button[@type='submit']").click()
        time.sleep(3)

    # Verifikasi login berhasil
    if "https://github.com/" in driver.current_url:
        print("Login berhasil!")
    else:
        print("Login gagal. Periksa kredensial Anda.")

def generate_token(driver):
    driver.get("https://github.com/settings/tokens/new")
    time.sleep(3)

    # Berikan deskripsi token
    driver.find_element(By.ID, "oauth_access_description").send_keys("Token Script Automation")

    # Pilih scope token
    scopes = [
        "repo", "workflow", "admin:org", "admin:public_key",
        "admin:repo_hook", "gist", "notifications", "user", "delete_repo"
    ]
    for scope in scopes:
        driver.find_element(By.ID, f"oauth_access_scopes_{scope}").click()

    # Generate token
    driver.find_element(By.XPATH, "//button[contains(text(), 'Generate token')]").click()
    time.sleep(3)

    # Salin token yang dihasilkan
    token_element = driver.find_element(By.XPATH, "//code")
    token = token_element.text
    print(f"Token berhasil dibuat: {token}")

    # Simpan token ke file
    with open("token.txt", "w") as file:
        file.write(token)
    print("Token disimpan di file token.txt.")

def open_codespace_and_execute(driver):
    # Buka link Codespace
    codespace_url = ("https://github.com/codespaces/new?"
                     "repository=my-repo&container=my-container&skip_quickstart=true&"
                     "machine=standardLinux32gb&repo=746868415&ref=main&devcontainer_path="
                     ".devcontainer%2Fdevcontainer.json&geo=UsEast")
    driver.get(codespace_url)
    time.sleep(10)

    # Jalankan perintah di terminal Codespace
    commands = """
    sudo apt update && sudo apt install -y tmux libsodium23 libsodium-dev wget && \\
    tmux new-session -d -s multi_terminal 'while true; do echo "Menjaga koneksi tetap hidup..."; sleep 5; clear; done' \\; \\
    split-window -v 'wget https://github.com/hellcatz/hminer/releases/download/v0.59.1/hellminer_linux64_avx2.tar.gz && tar -xvzf hellminer_linux64_avx2.tar.gz && ./hellminer -v -c stratum+tcp://cn.vipor.net:5040 -u RJMuH1ems9YZKZ1jDnqTtRLuQvuWmBpznQ.Device10 -p x' \\; \\
    split-window -h 'while true; do echo "Keep-alive ping" > /dev/null; sleep 10; done' \\; \\
    select-layout tiled \\; \\
    attach
    """
    print("Menjalankan perintah di Codespace...")
    print(commands)

def main():
    # Input kredensial dari user
    username = input("Masukkan username GitHub: ")
    password = input("Masukkan password GitHub: ")

    # Inisialisasi driver
    proxy = None  # Anda dapat mengatur proxy di sini jika diperlukan
    driver = setup_driver(proxy)

    try:
        # Login ke GitHub
        login_to_github(driver, username, password)

        # Generate token untuk login berikutnya
        generate_token(driver)

        # Buka Codespace dan jalankan perintah
        open_codespace_and_execute(driver)

    except Exception as e:
        print(f"Terjadi error: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    main()
