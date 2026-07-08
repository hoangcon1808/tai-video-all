Dưới đây là nội dung chuẩn cho file **README.md** của dự án. Bạn chỉ cần tạo file tên README.md trong thư mục gốc và sao chép toàn bộ nội dung dưới đây vào, giao diện hiển thị trên GitHub hoặc GitLab sẽ cực kỳ chuyên nghiệp và rõ ràng!
```markdown
# ⚡ Universal Video & Audio Downloader Pro 🎬🎵

![Python](https://img.shields.io/badge/Python-3.9%2B-blue?style=for-the-badge&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.110.0-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![TailwindCSS](https://img.shields.io/badge/Tailwind_CSS-38B2AC?style=for-the-badge&logo=tailwind-css&logoColor=white)
![Vercel](https://img.shields.io/badge/Vercel-Deploy-000000?style=for-the-badge&logo=vercel&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)

Một ứng dụng web đa nền tảng cho phép tải video (MP4) và âm thanh (MP3) chất lượng cao từ hơn 1.000+ trang web khác nhau như **YouTube, Facebook, Instagram, TikTok, X (Twitter)...** Dự án được tối ưu hóa đặc biệt để triển khai trên **Vercel Serverless Functions**, tích hợp cơ chế **Proxy vượt rào CORS** và giả lập User-Agent di động giúp tải video từ các mạng xã hội một cách trơn tru, không bị lỗi tường lửa hay yêu cầu đăng nhập.

---

## 🔥 Tính Năng Nổi Bật

- **🌐 Hỗ Trợ Đa Nền Tảng:** Nhận diện và tải video/âm thanh từ YouTube, TikTok, Facebook Watch/Reels, Instagram Stories/Reels, X (Twitter), Threads...
- **🎬 vs 🎵 Chuyển Đổi Định Dạng:** Nút gạt thông minh cho phép chọn tải về file **Video (MP4)** với các độ phân giải (1080p, 720p, 480p, 360p) hoặc file **Âm thanh (MP3)** chất lượng cao (320kbps, 192kbps, 128kbps).
- **🛡️ Vượt CORS & Bypass Tường Lửa:** - Tích hợp Proxy trung gian trên Backend Python giúp tải file trực tiếp mà không bị trình duyệt chặn (CORS Error).
  - Tự động giả lập Header của thiết bị iPhone (iOS Safari) để vượt rào cản đăng nhập của Facebook và Instagram.
- **🧹 Tự Động Làm Sạch URL (Auto-Sanitizer):** Tự động cắt bỏ các tham số theo dõi rác (`?igsh=...`, `?fbclid=...`, `?mibextid=...`) giúp link gọn gàng và tránh lỗi phân tích.
- **✨ Giao Diện Dark Mode Siêu Mượt:** Thiết kế bằng Tailwind CSS sắc nét, bố cục hiện đại, tích hợp hiệu ứng chuyển động và tương tác tốt trên cả PC lẫn điện thoại.
- **📋 Smart Clipboard & Toast Notification:** - Hệ thống thông báo **Toast** góc màn hình thay thế hoàn toàn `alert()`/`prompt()` gây phiền phức.
  - Xử lý Copy/Paste thông minh, tự động xin quyền hoặc hướng dẫn người dùng thao tác nếu trình duyệt bảo mật cao.
- **🕒 Quản Lý Lịch Sử & Hàng Đợi:** Tự động lưu lại các liên kết đã tải hoặc thêm vào danh sách chờ trực tiếp trên `localStorage` của trình duyệt.
- **⚡ Force Download:** Sử dụng cơ chế tải ngầm bằng JavaScript giúp ép tải file về máy ngay lập tức mà không bị trình duyệt tự động mở sang tab mới.

---

## 🛠️ Công Nghệ Sử Dụng

- **Backend:** Python 3, FastAPI, Uvicorn, yt-dlp, Requests.
- **Frontend:** HTML5, Tailwind CSS (via CDN), Vanilla JavaScript hiện đại (Async/Await, DOM Manipulation).
- **Hosting / Deployment:** Vercel (Python Serverless Functions & Static Hosting).

---

## 📁 Cấu Trúc Dự Án

```text
video-downloader/
│
├── api/
│   └── index.py        # Backend FastAPI: Xử lý trích xuất link (yt-dlp) & Proxy Stream
│
├── index.html          # Giao diện Frontend duy nhất (Đặt tại gốc để Vercel đọc trực tiếp)
├── requirements.txt    # Danh sách thư viện Python cần thiết
├── vercel.json         # Cấu hình định tuyến (Routing & Builders) cho Vercel
└── README.md           # Tài liệu hướng dẫn dự án

```
## 🚀 Hướng Dẫn Cài Đặt & Chạy Cục Bộ (Local)
### 1. Yêu cầu hệ thống
 * Máy tính đã cài đặt **Python 3.9+**.
 * Đã cài đặt **Git** và **Node.js** (để dùng Vercel CLI - tùy chọn).
### 2. Các bước cài đặt
**Bước 1:** Clone dự án về máy:
```bash
git clone [https://github.com/your-username/video-downloader.git](https://github.com/your-username/video-downloader.git)
cd video-downloader

```
**Bước 2:** Cài đặt các thư viện Python:
```bash
pip install -r requirements.txt

```
**Bước 3:** Khởi chạy Backend FastAPI cục bộ:
```bash
uvicorn api.index:app --reload --port 8000

```
*Backend sẽ chạy tại: http://localhost:8000*
**Bước 4:** Mở file index.html trực tiếp bằng trình duyệt hoặc sử dụng extension **Live Server** trên VS Code để trải nghiệm. *(Lưu ý: Nếu chạy local, bạn cần sửa biến const API_BASE = '/api'; trong file index.html thành http://localhost:8000/api để Frontend kết nối đúng với Backend).*
## ☁️ Hướng Dẫn Triển Khai Lên Vercel (Deploy)
Dự án này được thiết kế để triển khai lên Vercel **chỉ trong 1 phút** mà không cần cấu hình phức tạp.
### Cách 1: Triển khai bằng Vercel CLI (Nhanh nhất)
 1. Cài đặt Vercel CLI trên terminal:
   ```bash
   npm i -g vercel
   
   ```
 2. Mở terminal tại thư mục gốc của dự án và chạy lệnh:
   ```bash
   vercel --prod
   
   ```
 3. Nhấn Enter để chấp nhận các thiết lập mặc định. Vercel sẽ tự động tải thư viện Python, build serverless function và cung cấp cho bạn đường link HTTPS hoàn chỉnh!
### Cách 2: Triển khai qua GitHub
 1. Đẩy (Push) toàn bộ code này lên một Repository mới trên GitHub của bạn.
 2. Đăng nhập vào Vercel Dashboard, chọn **Add New Project**.
 3. Import Repository vừa tạo từ GitHub.
 4. Giữ nguyên mọi cấu hình mặc định và nhấn **Deploy**.
## ⚠️ Lưu Ý & Miễn Trừ Trách Nhiệm (Disclaimer)
 * Công cụ này được phát triển với mục đích **học tập, nghiên cứu kỹ thuật** xử lý API, Serverless và vượt lỗi CORS.
 * yt-dlp là một thư viện mã nguồn mở liên tục được cập nhật. Nếu một ngày nào đó việc tải video từ một nền tảng nhất định bị lỗi, hãy đảm bảo bạn đã cập nhật phiên bản yt-dlp mới nhất trong requirements.txt.
 * Vui lòng tôn trọng bản quyền tác giả và quyền riêng tư của người sáng tạo nội dung. Không sử dụng công cụ này để tải và phát tán các video/âm thanh bản quyền cho mục đích thương mại trái phép.
## 🤝 Đóng Góp & Liên Hệ
Mọi ý kiến đóng góp, báo lỗi (Issue) hoặc Pull Request đều được hoan nghênh để dự án ngày càng hoàn thiện hơn!
 * **Tác giả:** [Tên của bạn / Nickname]
 * **Giấy phép:** MIT License
```

```
