import shutil
import tempfile
from pathlib import Path

from fastapi import FastAPI, UploadFile, File, HTTPException

from local_ocr.ocr import run_ocr, save_result

app = FastAPI(title="OCR Workbench API")

# File types we allow
ALLOWED_TYPES: set[str] = {".pdf", ".png", ".jpg", ".jpeg", ".tiff", ".bmp"}


@app.get("/")
def home() -> dict:
    """A simple message so you know the API is alive."""
    return {"message": "OCR Workbench API is running. Go to /docs to upload a file."}


@app.post("/ocr/local")
async def ocr_local(file: UploadFile = File(...)) -> dict:
    """
    Upload an image or PDF. Runs local OCR and returns the extracted text.
    Also saves the result as a JSON file in the results folder.
    """
    # Check the file type is one we support
    suffix = Path(file.filename).suffix.lower()
    if suffix not in ALLOWED_TYPES:
        raise HTTPException(
            status_code=400,
            detail=f"File type '{suffix}' is not supported. Allowed: {sorted(ALLOWED_TYPES)}",
        )

    # Save the uploaded file to a temporary spot on disk so OCR can read it
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        shutil.copyfileobj(file.file, tmp)
        tmp_path = tmp.name

    try:
        result = run_ocr(tmp_path)
        # Fix the file name in the result to the real uploaded name, not the temp name
        result["file"] = file.filename
        saved_path = save_result(result)
        result["saved_to"] = saved_path
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"OCR failed: {str(e)}")
    finally:
        # Clean up the temporary file
        Path(tmp_path).unlink(missing_ok=True)