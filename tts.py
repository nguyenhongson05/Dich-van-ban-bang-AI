from gtts import gTTS
import os
import uuid

# Thư mục lưu audio
BASE_DIR = os.path.dirname(os.path.dirname(__file__))  # lên 1 cấp so với services/
AUDIO_DIR = os.path.join(BASE_DIR, "uploads", "audio")
os.makedirs(AUDIO_DIR, exist_ok=True)

# Ngôn ngữ TTS mặc định là tiếng Việt
DEFAULT_LANG = "vi"

def text_to_speech(text: str, lang: str = DEFAULT_LANG) -> str:
    """
    Chuyển văn bản thành giọng nói.
    Trả về đường dẫn relative để frontend có thể gọi: 'audio/filename.mp3'
    """
    try:
        filename = f"{uuid.uuid4().hex}.mp3"
        filepath = os.path.join(AUDIO_DIR, filename)

        tts = gTTS(text=text, lang=lang)
        tts.save(filepath)

        # Trả về đường dẫn relative để frontend dùng URL: /audio/filename.mp3
        return f"audio/{filename}"
    except Exception as e:
        return f"Error: {e}"
