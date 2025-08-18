# main.py
from fastapi import FastAPI, Form, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, FileResponse
from gtts import gTTS
from googletrans import Translator
import os
import uuid
from PIL import Image
import pytesseract

app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

# Chỉ đường dẫn đến Tesseract (Windows)
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# Thư mục lưu audio
AUDIO_DIR = "audio"
os.makedirs(AUDIO_DIR, exist_ok=True)

translator = Translator()

# ---------------- Text Translation ----------------
@app.post("/translate")
async def translate(text: str = Form(...), target_lang: str = Form(...)):
    try:
        translated = translator.translate(text, dest=target_lang).text
        return {"translated": translated}
    except Exception as e:
        return {"error": f"Lỗi dịch: {e}"}

# ---------------- File / Ảnh Translation ----------------
@app.post("/translate-file")
async def translate_file(
    file: UploadFile = File(...),
    target_lang: str = Form(...),
    ocr_lang: str = Form("eng")  # mặc định OCR tiếng Anh
):
    try:
        content = await file.read()
        text = ""

        # Nếu là file text
        if file.filename.endswith(".txt"):
            text = content.decode("utf-8", errors="ignore")

        # Nếu là ảnh
        elif file.filename.lower().endswith((".jpg", ".jpeg", ".png")):
            temp_path = f"temp_{uuid.uuid4()}.png"
            with open(temp_path, "wb") as f:
                f.write(content)
            image = Image.open(temp_path)
            text = pytesseract.image_to_string(image, lang=ocr_lang)  # OCR theo ngôn ngữ chọn
            os.remove(temp_path)

        else:
            return {"error": "Chỉ hỗ trợ .txt hoặc ảnh (.jpg/.jpeg/.png)"}

        if not text.strip():
            return {"error": "Không nhận diện được chữ trong file/ảnh"}

        # Làm sạch text OCR
        text = text.replace("\n", " ").strip()

        # Dịch văn bản
        translated = translator.translate(text, dest=target_lang).text
        return {"original": text, "translated": translated}

    except Exception as e:
        return {"error": f"Lỗi dịch file: {e}"}

# ---------------- Text-to-Speech ----------------
@app.post("/tts")
async def tts(text: str = Form(...), lang: str = Form(...)):
    try:
        file_id = str(uuid.uuid4())
        filename = f"{file_id}.mp3"
        filepath = os.path.join(AUDIO_DIR, filename)
        tts = gTTS(text=text, lang=lang)
        tts.save(filepath)
        return {"audio_file": f"{AUDIO_DIR}/{filename}"}
    except Exception as e:
        return {"error": f"Lỗi tạo audio: {e}"}

# ---------------- Lấy Audio ----------------
@app.get("/audio/{file_name}")
def get_audio(file_name: str):
    path = os.path.join(AUDIO_DIR, file_name)
    if os.path.exists(path):
        return FileResponse(path, media_type="audio/mpeg")
    return JSONResponse({"error": "File không tồn tại"}, status_code=404)
