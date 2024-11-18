Berikut adalah README.md yang dapat Anda gunakan untuk mendokumentasikan cara penggunaan script utama (main.py) dan script penginstalan modul di berbagai platform:


---

Panduan Penggunaan Script GitHub Automation

Script ini dirancang untuk mengelola akun GitHub Anda secara otomatis, termasuk login, mengelola Codespace, dan menjalankan perintah di dalamnya. Berikut adalah langkah-langkah instalasi dan penggunaan script di berbagai platform: Linux, Windows, dan Termux.


---

1. Persyaratan

Python 3.7 atau lebih tinggi

Pip (Python Package Manager)

Browser Google Chrome

Akses internet yang stabil



---

2. Cara Instalasi

2.1. Di Linux

1. Perbarui sistem dan instal Python:

sudo apt update && sudo apt upgrade -y
sudo apt install -y python3 python3-pip wget


2. Unduh script installer dan script utama:

wget https://example.com/installer.py -O installer.py
wget https://example.com/main.py -O main.py


3. Jalankan script penginstalan modul:

python3 installer.py


4. Jalankan script utama:

python3 main.py




---

2.2. Di Windows

1. Unduh dan instal Python
Download Python.
Pastikan untuk mencentang Add Python to PATH saat instalasi.


2. Buka Command Prompt (CMD) dan instal pip jika belum ada:

python -m ensurepip --upgrade


3. Unduh script installer dan script utama:

curl -o installer.py https://example.com/installer.py
curl -o main.py https://example.com/main.py


4. Jalankan script penginstalan modul:

python installer.py


5. Jalankan script utama:

python main.py




---

2.3. Di Termux

1. Perbarui Termux dan instal Python:

pkg update && pkg upgrade -y
pkg install -y python wget


2. Unduh script installer dan script utama:

wget https://example.com/installer.py -O installer.py
wget https://example.com/main.py -O main.py


3. Jalankan script penginstalan modul:

python installer.py


4. Jalankan script utama:

python main.py




---

3. Cara Penggunaan Script Utama (main.py)

Langkah-Langkah:

1. Jalankan script utama:

python main.py


2. Masukkan informasi akun GitHub sesuai prompt:

Masukkan username GitHub:
Ketik username akun GitHub Anda.

Masukkan password GitHub:
Ketik password akun GitHub Anda.

Masukkan OTP (jika diminta):
Jika GitHub meminta kode OTP, masukkan kode yang dikirimkan ke perangkat Anda.



3. Script akan:

Login ke akun GitHub.

Generate token untuk login berikutnya dan menyimpannya di token.txt.

Membuka Codespace sesuai dengan URL yang telah diatur.

Menjalankan perintah di dalam Codespace.



4. Setelah semua proses selesai, monitoring akan berjalan di terminal. Status akun akan ditampilkan, termasuk apakah Codespace berjalan dengan baik atau tidak.




---

4. Troubleshooting

Error: WebDriver Tidak Ditemukan

Pastikan browser Google Chrome terinstal di perangkat Anda.

Jalankan kembali installer.py untuk menginstal WebDriver.


Error: Modul Tidak Ditemukan

Jalankan kembali:

python installer.py



---

5. Catatan

Keamanan Data Login: Jangan bagikan informasi username, password, atau OTP Anda kepada siapa pun.

Proxy Scraping: Script ini menggunakan proxy untuk login akun GitHub dengan identitas yang berbeda.

File token.txt: File ini menyimpan token login GitHub Anda untuk login berikutnya. Pastikan file ini tersimpan dengan aman.


