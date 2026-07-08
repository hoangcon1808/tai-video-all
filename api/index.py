from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
import yt_dlp
import requests
import urllib.parse
import re

app = FastAPI()

# Bật CORS tối đa cho trình duyệt không chặn
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["Content-Disposition"]
)

@app.get("/api/extract")
def extract_video_info(url: str = Query(...)):
    if not url:
        raise HTTPException(status_code=400, detail="Vui lòng cung cấp URL")
    
    ydl_opts = {
        'format': 'best',
        'quiet': True,
        'no_warnings': True,
        'skip_download': True,
        'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            
            formats = []
            for f in info.get('formats', []):
                if f.get('url') and (f.get('vcodec') != 'none' or f.get('acodec') != 'none'):
                    quality = f.get('format_note') or f.get('resolution') or f'{f.get("height", "N/A")}p'
                    formats.append({
                        'format_id': f.get('format_id'),
                        'ext': f.get('ext', 'mp4'),
                        'quality': quality,
                        'url': f.get('url'),
                        'has_audio': f.get('acodec') != 'none',
                        'has_video': f.get('vcodec') != 'none'
                    })
            
            formats.reverse()

            return {
                "success": True,
                "title": info.get('title', 'Video_Tải_Về'),
                "thumbnail": info.get('thumbnail'),
                "duration": info.get('duration'),
                "platform": info.get('extractor_key'),
                "formats": formats[:15],
                "direct_url": info.get('url') or (formats[0]['url'] if formats else None)
            }
    except Exception as e:
        raise HTTPException(status_code=500, detail="Không thể phân tích link: " + str(e))

@app.get("/api/proxy")
def proxy_download(url: str = Query(...), filename: str = Query("video.mp4")):
    try:
        # Làm sạch tên file để trình duyệt không bị lỗi ký tự đặc biệt
        safe_filename = re.sub(r'[\\/*?:"<>|]', "", filename)
        encoded_filename = urllib.parse.quote(safe_filename)
        
        req = requests.get(url, stream=True, headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'
        })
        
        return StreamingResponse(
            req.iter_content(chunk_size=16384),
            media_type=req.headers.get("content-type", "video/mp4"),
            headers={
                "Content-Disposition": f"attachment; filename*=UTF-8''{encoded_filename}",
                "Access-Control-Expose-Headers": "Content-Disposition"
            }
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail="Lỗi proxy: " + str(e))
