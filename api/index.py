from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
import yt_dlp
import requests

app = FastAPI()

# Bật CORS cho phép mọi nguồn truy cập
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/extract")
def extract_video_info(url: str = Query(..., description="URL của video cần tải")):
    if not url:
        raise HTTPException(status_code=400, detail="Vui lòng cung cấp URL")
    
    ydl_opts = {
        'format': 'best',
        'quiet': True,
        'no_warnings': True,
        'skip_download': True,
        'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            
            # Lấy các định dạng video/audio
            formats = []
            for f in info.get('formats', []):
                if f.get('url') and (f.get('vcodec') != 'none' or f.get('acodec') != 'none'):
                    quality = f.get('format_note') or f.get('resolution') or f'{f.get("height", "N/A")}p'
                    formats.append({
                        'format_id': f.get('format_id'),
                        'ext': f.get('ext'),
                        'quality': quality,
                        'url': f.get('url'),
                        'has_audio': f.get('acodec') != 'none',
                        'has_video': f.get('vcodec') != 'none'
                    })
            
            # Sắp xếp chất lượng từ cao xuống thấp
            formats.reverse()

            return {
                "success": True,
                "title": info.get('title', 'Video Không Tên'),
                "thumbnail": info.get('thumbnail'),
                "duration": info.get('duration'),
                "platform": info.get('extractor_key'),
                "formats": formats[:15],
                "direct_url": info.get('url') or (formats[0]['url'] if formats else None)
            }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/proxy")
def proxy_download(url: str = Query(...), filename: str = Query("video.mp4")):
    """
    Proxy stream giúp vượt CORS khi tải file từ các nguồn chặn truy cập trực tiếp từ trình duyệt
    """
    try:
        req = requests.get(url, stream=True, headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        })
        return StreamingResponse(
            req.iter_content(chunk_size=8192),
            media_type=req.headers.get("content-type", "application/octet-stream"),
            headers={"Content-Disposition": f'attachment; filename="{filename}"'}
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail="Lỗi khi proxy file: " + str(e))
