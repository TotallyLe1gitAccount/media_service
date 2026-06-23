import magic

MAX_FILE_SIZE = 100 * 1024 * 1024
ALLOWED_MIME_TYPES = {
        "video/mp4",
        "video/webm",
    }

class VideoValidator:
    def validate_metadata(self, info : dict) -> tuple[bool, dict[str , str]]:
        streams = info.get("streams", [])
        format_info = info.get("format", {})

        video_stream = None
        audio_stream = None

        for s in streams:
            if s.get("codec_type") == "video":
                video_stream = s
            if s.get("codec_type") == "audio":
                audio_stream = s

        if not video_stream:
            return False, {"code": "no_video_stream"}
        
        if video_stream.get("codec_name") != "h264":
            return False, {"code": "unsupported_video_content"}
        
        width = video_stream.get("width", 0)
        height = video_stream.get("height", 0)

        if width > 1920 or height > 1080:
            return False, {"code": "resolution_too_high"}
        
        try:
            num, den = map(int, video_stream.get("avg_frame_rate", "0/1").split("/"))
            fps = num / den if den else 0
        except:
            fps = 0

        if fps > 60:
            return False, {"code": "fps_too_high"}
        elif fps <= 0:
            return False, {"code" : "fps_too_low"}
        
        duration = float(format_info.get("duration", 0))

        if duration > 600:
            return False, {"code" : "video_too_long"}
        elif duration <= 0:
            return False, {"code" : "video_too_short"}
        
        return True, {"code" : "OK"}

    async def validate_size(self, file) -> bool:
        file.file.seek(0, 2)
        size = file.file.tell()
        file.file.seek(0)

        return size <= MAX_FILE_SIZE

    async def validate_content(self, file) -> bool:
        content = await file.read(2048)
        await file.seek(0)

        return magic.from_buffer(content, mime=True) in ALLOWED_MIME_TYPES
    


