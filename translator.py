# services/translator.py
from googletrans import Translator

translator = Translator()

def translate_text(text: str, target_lang: str) -> str:
    """
    Dịch văn bản sang ngôn ngữ target_lang.
    Nếu lỗi xảy ra, trả về văn bản gốc.
    """
    if not text.strip():
        return ""
    
    try:
        result = translator.translate(text, dest=target_lang)
        return result.text
    except Exception as e:
        # log lỗi ra console, không dừng app
        print(f"[translate_text] Lỗi khi dịch: {e}")
        return text
