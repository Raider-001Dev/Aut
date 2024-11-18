import os
import subprocess
import sys

def install_modules():
    """Install required Python modules."""
    print("Menginstal modul yang diperlukan...")
    required_modules = ["selenium", "requests", "webdriver-manager"]
    
    for module in required_modules:
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", module])
            print(f"Modul '{module}' berhasil diinstal.")
        except subprocess.CalledProcessError:
            print(f"Gagal menginstal modul '{module}'.")
            sys.exit(1)
    print("Semua modul berhasil diinstal.")

def install_webdriver():
    """Install WebDriver using webdriver-manager."""
    print("Menginstal WebDriver menggunakan webdriver-manager...")
    try:
        from selenium import webdriver
        from webdriver_manager.chrome import ChromeDriverManager
        from selenium.webdriver.chrome.service import Service
        
        # Install ChromeDriver
        service = Service(ChromeDriverManager().install())
        print("WebDriver berhasil diinstal dan dikonfigurasi.")
        
    except Exception as e:
        print(f"Terjadi kesalahan saat menginstal WebDriver: {e}")
        sys.exit(1)

def main():
    print("Menyiapkan lingkungan untuk script...")
    
    # Install Python modules
    install_modules()
    
    # Install WebDriver
    install_webdriver()
    
    print("\nLingkungan berhasil disiapkan. Anda siap menjalankan script utama!")

if __name__ == "__main__":
    main()
