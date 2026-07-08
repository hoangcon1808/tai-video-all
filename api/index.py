from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
import yt_dlp
import requests
import urllib.parse
import re

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["Content-Disposition"]
)

def clean_social_url(url: str) -> str:
    clean_url = re.sub(r'([?&])(igsh|mibextid|fbclid|utm_[^&]+|share_id|si|ref|loc)=[^&]*', r'\1', url)
    clean_url = re.sub(r'[?&]$', '', clean_url)
    return clean_url

@app.get("/api/extract")
def extract_video_info(url: str = Query(...)):
    if not url:
        raise HTTPException(status_code=400, detail="Vui lòng cung cấp URL")
    
    url = clean_social_url(url.trim() if hasattr(url, 'trim') else url.strip())
    
    # Cấu hình yt-dlp tối ưu lấy cả video lẫn audio chất lượng cao
    ydl_opts = {
        'format': 'bestvideo+bestaudio/best',
        'quiet': True,
        'no_warnings': True,
        'skip_download': True,
        'nocheckcertificate': True,
        'ignoreerrors': False,
        'http_headers': {
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.9',
            'Sec-Fetch-Mode': 'navigate',
        }
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            
            if 'entries' in info and info['entries']:
                info = info['entries'][0]
            
            formats = []
            for f in info.get('formats', []):
                if f.get('url') and (f.get('vcodec') != 'none' or f.get('acodec') != 'none'):
                    is_audio_only = (f.get('vcodec') == 'none' and f.get('acodec') != 'none')
                    
                    # Tạo nhãn chất lượng riêng cho Video và Audio
                    if is_audio_only:
                        tbr = f.get('tbr') or f.get('abr')
                        quality = f"{int(tbr)}kbps (Audio)" if tbr else "Âm thanh gốc"
                        ext = 'mp3'
                    else:
                        quality = f.get('format_note') or f.get('resolution') or f'{f.get("height", "N/A")}p'
                        ext = f.get('ext', 'mp4')

                    formats.append({
                        'format_id': f.get('format_id'),
                        'ext': ext,
                        'quality': quality,
                        'url': f.get('url'),
                        'has_audio': f.get('acodec') != 'none',
                        'has_video': f.get('vcodec') != 'none',
                        'is_audio_only': is_audio_only
                    })
            
            formats.reverse()

            extractor = info.get('extractor_key', 'Video').lower()
            if 'facebook' in extractor: platform = 'Facebook'
            elif 'instagram' in extractor: platform = 'Instagram'
            elif 'tiktok' in extractor: platform = 'TikTok'
            elif 'youtube' in extractor: platform = 'YouTube'
            else: platform = info.get('extractor_key', 'Video')

            return {
                "success": True,
                "title": info.get('title', f'{platform}_Video_Tải_Về'),
                "thumbnail": info.get('thumbnail'),
                "duration": info.get('duration'),
                "platform": platform,
                "formats": formats[:20], # Tăng số lượng định dạng trả về
                "direct_url": info.get('url') or (formats[0]['url'] if formats else None)
            }
    except Exception as e:
        raise HTTPException(status_code=500, detail="Không thể tải link này. Đảm bảo video để ở chế độ Công Khai! Chi tiết: " + str(e))

@app.get("/api/proxy")
def proxy_download(url: str = Query(...), filename: str = Query("video.mp4")):
    try:
        safe_filename = re.sub(r'[\\/*?:"<>|]', "", filename)
        encoded_filename = urllib.parse.quote(safe_filename)
        
        req = requests.get(url, stream=True, headers={
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1',
            'Referer': 'https://www.google.com/'
        })
        
        # Xác định Content-Type dựa trên phần mở rộng của file tải về
        content_type = "audio/mpeg" if safe_filename.endswith(('.mp3', '.m4a')) else "video/mp4"
        
        return StreamingResponse(
            req.iter_content(chunk_size=16384),
            media_type=req.headers.get("content-type", content_type),
            headers={
                "Content-Disposition": f"attachment; filename*=UTF-8''{encoded_filename}",
                "Access-Control-Expose-Headers": "Content-Disposition"
            }
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail="Lỗi proxy: " + str(e))
