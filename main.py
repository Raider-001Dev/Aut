from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time


def setup_driver(proxy=None):
    chrome_options = Options()
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("--disable-extensions")
    
    if proxy:
        chrome_options.add_argument(f'--proxy-server={proxy}')
    
    service = Service("/usr/bin/chromedriver")  # Path to ChromeDriver
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver


def login(driver):
    try:
        print("Masukkan username: ")
        username = input()
        print("Masukkan password: ")
        password = input()

        # Akses halaman login
        driver.get("https://example.com/login")

        # Tunggu elemen input username muncul
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "username_input_id")))
        username_field = driver.find_element(By.ID, "username_input_id")
        username_field.send_keys(username)

        # Tunggu elemen input password muncul
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "password_input_id")))
        password_field = driver.find_element(By.ID, "password_input_id")
        password_field.send_keys(password)

        # Klik tombol login
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "login_button_id")))
        login_button = driver.find_element(By.ID, "login_button_id")
        login_button.click()

        print("Login berhasil!")
    except Exception as e:
        print(f"Terjadi error saat login: {e}")


def main():
    # Setup driver
    proxy = None  # Masukkan proxy jika diperlukan
    driver = setup_driver(proxy)

    try:
        # Login ke website
        login(driver)
        
        # Tambahkan logika tambahan jika perlu setelah login
        print("Menjalankan proses tambahan...")
        time.sleep(5)

    except Exception as e:
        print(f"Terjadi error di main: {e}")
    finally:
        driver.quit()


if __name__ == "__main__":
    main()
