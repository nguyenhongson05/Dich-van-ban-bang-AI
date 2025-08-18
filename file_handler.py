import os
from PyPDF2 import PdfReader
import docx
from PIL import Image
import pytesseract

def extract_text_from_file(file_path: str) -> str:
    ext = os.path.splitext(file_path)[1].lower()
    try:
        if ext == ".txt":
            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                return f.read()

        elif ext == ".pdf":
            text = ""
            reader = PdfReader(file_path)
            for page in reader.pages:
                text += page.extract_text() or ""
            return text.strip()

        elif ext in [".docx", ".doc"]:
            doc = docx.Document(file_path)
            return "\n".join([para.text for para in doc.paragraphs if para.text.strip()])

        elif ext in [".jpg", ".jpeg", ".png", ".bmp", ".tiff"]:
            image = Image.open(file_path)
            text = pytesseract.image_to_string(image, lang="vie+eng")
            return text.strip()

        else:
            return "Unsupported file format"
    except Exception as e:
        return f"Error reading file: {e}"
