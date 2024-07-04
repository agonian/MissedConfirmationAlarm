import tkinter as tk
from tkinter import messagebox
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time
from bs4 import BeautifulSoup
import winsound
import threading
import os
import sys
import tempfile
import shutil
import telepot

# Telegram bot token
TELEGRAM_TOKEN = '6572807845:AAEPc3qMsD3M3IKZFzCE-lCcP7UcgV1vACg'
bot = telepot.Bot(TELEGRAM_TOKEN)

def play_error_sound():
    frequency = 2500  # Frekansı ayarlayabilirsiniz (örneğin, 2500 Hz)
    duration = 1000   # Süreyi ayarlayabilirsiniz (örneğin, 1000 milisaniye = 1 saniye)
    winsound.Beep(frequency, duration)

# ChromeDriver'ın geçici dizini
chrome_driver_path = None

def extract_chromedriver():
    global chrome_driver_path
    # PyInstaller tarafından oluşturulan geçici dizini al
    temp_dir = getattr(sys, '_MEIPASS', os.path.abspath(os.path.dirname(__file__)))
    
    # ChromeDriver'ı geçici dizine çıkar
    chromedriver_src = os.path.join(temp_dir, 'chromedriver.exe')
    chromedriver_dest = os.path.join(tempfile.mkdtemp(), 'chromedriver.exe')
    shutil.copy(chromedriver_src, chromedriver_dest)
    
    # ChromeDriver yolunu güncelle
    chrome_driver_path = chromedriver_dest

def run_bot(url, chat_id):
    global running, chrome_driver_path
    
    # ChromeDriver'ı çıkar
    extract_chromedriver()
    
    # Chrome seçenekleri
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Tarayıcıyı arka planda çalıştırmak için

    # WebDriver servisini başlatın
    service = Service(chrome_driver_path)
    driver = webdriver.Chrome(service=service, options=chrome_options)

    # Tarayıcıyı başlatın ve web sayfasına gidin
    driver.get(url)

    # Daha önce kontrol edilen linklerin listesi
    checked_links = set()

    try:
        while running:
            # Sayfa kaynağını al
            soup = BeautifulSoup(driver.page_source, 'html.parser')

            # Sayfadaki tüm <a> etiketlerini bul
            links = soup.find_all('a')

            for link in links:
                if not running:
                    break
                href = link.get('href')
                if href and href not in checked_links:
                    # Linkin içeriğini al
                    link_content = link.text.strip()
                    if 'Success' in link_content:
                        # Sadece blok numarasını al
                        block_number = href.split('/')[-1]
                        update_text(f"Successful block: {block_number}", "green")
                    elif 'Failed' in link_content:
                        block_number = href.split('/')[-1]
                        update_text(f"Failed block: {block_number}", "red")
                        play_error_sound()
                        send_telegram_message(chat_id, f"Failed block detected: {block_number}")

                    checked_links.add(href)

            # Her 1 saniyede bir yeni linkleri kontrol etmek için bekleyin
            time.sleep(1)
        else:
            update_text("İşlem durduruldu.", "black")

    except KeyboardInterrupt:
        print("Kontrol durduruldu.")

    finally:
        # Tarayıcıyı kapat
        driver.quit()

def send_telegram_message(chat_id, message):
    bot.sendMessage(chat_id, message)

def submit_address():
    global output_text, running
    running = False  # Mevcut çalışan işlemi durdur
    time.sleep(1)  # Önceki işlemin düzgünce kapanması için kısa bir gecikme ekle
    output_text.config(state=tk.NORMAL)
    output_text.delete(1.0, tk.END)  # Önceki logları temizle
    output_text.config(state=tk.DISABLED)
    running = True  # Yeni işlem için bayrağı tekrar true yap
    address = entry_address.get()
    chat_id = entry_chat_id.get()
    if address and chat_id:
        messagebox.showinfo("Address Submitted", f"Address: {address}\nChat ID: {chat_id}")
        url = 'https://testnet.crossfi.exploreme.pro/validators/' + address  # Kontrol etmek istediğiniz URL
        threading.Thread(target=run_bot, args=(url, chat_id)).start()  # run_bot fonksiyonunu ayrı bir thread'de çalıştır
    else:
        messagebox.showwarning("Input Error", "Please enter both an address and chat ID.")

def update_text(text, color):
    if "Successful block:" in text or "Failed block:" in text:
        output_text.config(state=tk.NORMAL)
        output_text.insert(tk.END, text + "\n", color)
        output_text.config(state=tk.DISABLED)
        output_text.see(tk.END)
        output_text.update()  # Güncelleme ekleniyor

def exit_program():
    global running
    running = False
    root.quit()
    root.destroy()

def on_hover(event):
    event.widget.config(bg="lightblue")

def on_leave(event):
    event.widget.config(bg="SystemButtonFace")

# Ana pencere
root = tk.Tk()
root.title("Address Form")
root.resizable(False, False)  # Pencere boyutunu değiştirilemez yap

# Adres etiketi ve giriş
tk.Label(root, text="Enter Address:").grid(row=0, column=0, padx=10, pady=10)
entry_address = tk.Entry(root, width=50)
entry_address.grid(row=0, column=1, padx=10, pady=10)

# Chat ID etiketi ve giriş
tk.Label(root, text="Enter Chat ID:").grid(row=1, column=0, padx=10, pady=10)
entry_chat_id = tk.Entry(root, width=50)
entry_chat_id.grid(row=1, column=1, padx=10, pady=10)

# Chat ID'nin nasıl bulunacağını açıklayan etiket
chat_id_info = tk.Label(root, text="To find your chat ID, start a conversation with @userinfobot on Telegram and send '/start'.")
chat_id_info.grid(row=2, column=0, columnspan=2, padx=10, pady=5)

# Düğmeler çerçevesi
buttons_frame = tk.Frame(root)
buttons_frame.grid(row=3, column=1, padx=10, pady=10, sticky="e")

# Gönder düğmesi
submit_button = tk.Button(buttons_frame, text="Submit", command=submit_address)
submit_button.pack(side=tk.LEFT, padx=5)
submit_button.bind("<Enter>", on_hover)
submit_button.bind("<Leave>", on_leave)

# Çıkış düğmesi
exit_button = tk.Button(buttons_frame, text="Exit", command=exit_program)
exit_button.pack(side=tk.LEFT, padx=5)
exit_button.bind("<Enter>", on_hover)
exit_button.bind("<Leave>", on_leave)

# Çıktı metin alanı (Text kullanarak)
output_text = tk.Text(root, wrap=tk.WORD, width=80, height=20)
output_text.grid(row=4, column=0, columnspan=2, padx=10, pady=10)
output_text.config(state=tk.DISABLED)  # Başlangıçta düzenlenebilir olmasın

# Renk etiketlerini tanımla
output_text.tag_configure("green", foreground="green")
output_text.tag_configure("red", foreground="red")

# Tkinter olay döngüsünü başlat
root.mainloop()
