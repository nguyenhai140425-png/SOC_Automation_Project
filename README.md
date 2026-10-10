# SOC Automation Project - Malware Detection with VirusTotal & Discord Alerts

## 📌 Giới thiệu
Dự án này mô phỏng tư duy **SOC Analyst** trong việc tự động hóa quy trình phát hiện mã độc.  
Khi có file mới xuất hiện trong thư mục giám sát, chương trình sẽ:
- Tính toán **SHA256 hash** của file.
- Gửi hash lên **VirusTotal API** để kiểm tra.
- Nếu hash chưa có trên VirusTotal → tự động upload file để phân tích.
- Nếu phát hiện mã độc → gửi cảnh báo ngay lên **Discord Webhook**.

Dự án giúp minh họa cách một SOC Analyst có thể dùng **Python** để giảm tải công việc thủ công và tăng tốc độ phát hiện sự cố.

---

## ⚙️ Yêu cầu hệ thống
- Python 3.10+ (khuyến nghị dùng bản mới nhất).
- Mạng Internet để kết nối tới VirusTotal API và Discord.
- Tài khoản VirusTotal (để lấy API Key).
- Discord server với webhook đã tạo sẵn.

---

## 📂 Cấu trúc dự án
SOC_Automation_Project/
├── monitor.py          # File code chính
├── requirements.txt    # Danh sách thư viện cần cài
├── README.md           # Hướng dẫn sử dụng
├── .gitignore          # Bỏ qua các file/thư mục không cần push
├── watch_folder/       # Thư mục giám sát (rỗng, có .gitkeep)
│   └── .gitkeep
└── venv/               # Môi trường ảo (KHÔNG push lên GitHub)

---

## 📥 Cài đặt
1. Clone dự án:
   git clone https://github.com/username/SOC_Automation_Project.git
   cd SOC_Automation_Project
2.  Tạo môi trường ảo:

    python -m venv venv
    .\venv\Scripts\activate
3. Cài thư viện:

    pip install -r requirements.txt
4. Tạo file .env (KHÔNG push lên GitHub):

VT_API_KEY=your_virustotal_api_key
DISCORD_WEBHOOK_URL=your_discord_webhook_url
🚀 Chạy chương trình

python monitor.py

- Copy một file bất kỳ vào thư mục watch_folder/.

- Script sẽ tự động tính SHA256, gửi hash lên VirusTotal.

- Nếu hash chưa có → file sẽ được upload lên VirusTotal để phân tích.

- Nếu phát hiện mã độc → cảnh báo sẽ gửi ngay lên Discord.

📝 File .gitignore
# Bỏ môi trường ảo
venv/

# Bỏ file cấu hình môi trường
.env

# Bỏ các file tạm, cache
__pycache__/
*.pyc
*.pyo

# Bỏ thư mục giám sát nhưng giữ lại folder rỗng
watch_folder/*
!watch_folder/.gitkeep

# Bỏ các file hệ thống hoặc IDE
*.log
.vscode/
.idea/
💡 Ý nghĩa
Thể hiện tư duy Automation trong SOC.

Giúp giảm tải công việc thủ công, tăng tốc độ phát hiện sự cố.

Là một ví dụ thực tế để chứng minh khả năng dùng Python tối ưu hóa công việc của SOC Analyst.

Có thể mở rộng để tích hợp thêm các kênh cảnh báo khác (Telegram, Email, SIEM).

📌 Ghi chú
VirusTotal API có giới hạn số lượng request miễn phí mỗi ngày.

Nếu mạng chậm hoặc bị firewall chặn, có thể gặp lỗi ConnectTimeout. Hãy thêm timeout vào request hoặc thử mạng khác.

Không push file .env và venv/ lên GitHub để tránh lộ thông tin nhạy cảm và giảm dung lượng repo.