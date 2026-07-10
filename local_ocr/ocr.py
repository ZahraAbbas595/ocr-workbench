import json
import os
from pathlib import Path
from datetime import datetime

import pytesseract
from pdf2image import convert_from_path
from PIL import Image
from dotenv import load_dotenv

# Load the .env file so we can read TESSERACT_PATH and POPPLER_PATH
load_dotenv()

# Tell pytesseract where tesseract.exe lives on Windows
pytesseract.pytesseract.tesseract_cmd = os.getenv("TESSERACT_PATH", "tesseract")


def extract_text_from_image(image_path: str) -> str:
    """Open an image file and return the text found in it."""
    img = Image.open(image_path)
    text = pytesseract.image_to_string(img)
    return text.strip()


def extract_text_from_pdf(pdf_path: str) -> str:
    """Convert each PDF page to an image, run OCR on each, return all text joined."""
    poppler_path = os.getenv("POPPLER_PATH")
    pages = convert_from_path(pdf_path, poppler_path=poppler_path)
    all_text: list[str] = []
    for page in pages:
        text = pytesseract.image_to_string(page)
        all_text.append(text.strip())
    return "\n\n--- page break ---\n\n".join(all_text)


def run_ocr(file_path: str) -> dict:
    """
    Main function. Takes a file path, figures out if it is an image or PDF,
    runs OCR, and returns a result dictionary.
    """
    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    suffix = path.suffix.lower()

    if suffix == ".pdf":
        text = extract_text_from_pdf(file_path)
        file_type = "pdf"
    elif suffix in [".png", ".jpg", ".jpeg", ".tiff", ".bmp"]:
        text = extract_text_from_image(file_path)
        file_type = "image"
    else:
        raise ValueError(f"Unsupported file type: {suffix}")

    result: dict = {
        "source": "local_tesseract",
        "file": path.name,
        "file_type": file_type,
        "timestamp": datetime.utcnow().isoformat(),
        "text": text,
    }

    return result


def save_result(result: dict, output_dir: str = "results") -> str:
    """Save the OCR result as a JSON file. Returns the path it was saved to."""
    Path(output_dir).mkdir(exist_ok=True)
    filename = f"local_{Path(result['file']).stem}_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}.json"
    output_path = Path(output_dir) / filename
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)
    return str(output_path)