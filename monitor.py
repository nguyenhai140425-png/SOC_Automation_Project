import time
import os
import hashlib
import requests
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from dotenv import load_dotenv

# B1: Load API Key và Webhook URL từ file .env
load_dotenv()
VT_API_KEY = os.getenv("VT_API_KEY")
DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")

# B2: Hàm gửi cảnh báo lên Discord
def send_discord_alert(message):
    data = {"content": message}
    response = requests.post(DISCORD_WEBHOOK_URL, json=data)
    if response.status_code == 204:
        print("📩 Đã gửi cảnh báo lên Discord")
    else:
        print(f"❌ Lỗi khi gửi cảnh báo Discord: {response.status_code}")

# B3: Hàm kiểm tra hash trên VirusTotal
def check_virustotal(sha256_hash, file_path):
    url = f"https://www.virustotal.com/api/v3/files/{sha256_hash}"
    headers = {"x-apikey": VT_API_KEY}

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        malicious_count = data["data"]["attributes"]["last_analysis_stats"]["malicious"]

        if malicious_count > 0:
            alert_msg = f"⚠️ Phát hiện mã độc!\nFile: {file_path}\nHash: {sha256_hash}\nSố engines phát hiện: {malicious_count}"
            print(alert_msg)
            send_discord_alert(alert_msg)
        else:
            print("✅ File sạch (không phát hiện mã độc)")
    elif response.status_code == 404:
        print("ℹ️ Hash chưa có trên VirusTotal → Upload file để phân tích...")
        upload_to_virustotal(file_path)
    elif response.status_code == 401:
        print("❌ API Key không hợp lệ hoặc thiếu quyền")
    elif response.status_code == 429:
        print("❌ Quá giới hạn request của VirusTotal API")
    else:
        print(f"❌ Lỗi khác từ VirusTotal: {response.status_code}")
        print("Chi tiết phản hồi:", response.text)

# B4: Hàm upload file lên VirusTotal
def upload_to_virustotal(file_path):
    url = "https://www.virustotal.com/api/v3/files"
    headers = {"x-apikey": VT_API_KEY}
    with open(file_path, "rb") as f:
        files = {"file": f}
        response = requests.post(url, headers=headers, files=files)
    if response.status_code == 200:
        print("📤 File đã được upload lên VirusTotal để phân tích")
        send_discord_alert(f"📤 File {file_path} đã được upload lên VirusTotal để phân tích")
    elif response.status_code == 401:
        print("❌ API Key không hợp lệ khi upload")
    elif response.status_code == 429:
        print("❌ Quá giới hạn upload của VirusTotal API")
    else:
        print(f"❌ Lỗi khi upload file lên VirusTotal: {response.status_code}")
        print("Chi tiết phản hồi:", response.text)

# B5: Class giám sát thư mục
class MyHandler(FileSystemEventHandler):
    def on_created(self, event):
        if not event.is_directory:
            file_path = event.src_path
            print(f"File mới được tạo: {file_path}")

            # Tính SHA256
            with open(file_path, "rb") as f:
                file_data = f.read()
            sha256_hash = hashlib.sha256(file_data).hexdigest()
            print(f"SHA256: {sha256_hash}")

            # Gửi hash lên VirusTotal
            check_virustotal(sha256_hash, file_path)

# B6: Khởi động giám sát
if __name__ == "__main__":
    folder_to_watch = "watch_folder"  # Thư mục cần giám sát
    if not os.path.exists(folder_to_watch):
        os.makedirs(folder_to_watch)

    observer = Observer()
    observer.schedule(MyHandler(), folder_to_watch, recursive=False)
    observer.start()
    print(f"🔍 Đang giám sát thư mục: {folder_to_watch}")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
