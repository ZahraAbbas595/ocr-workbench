import shutil
import tempfile
from pathlib import Path

from fastapi import FastAPI, File, HTTPException, UploadFile

from local_ocr.ocr import run_ocr, save_result
from models import ALLOWED_FILE_TYPES, MAX_FILE_SIZE_BYTES, ConfigError, OCRResult

app = FastAPI(title="OCR Workbench API")

# File types we allow
ALLOWED_TYPES = ALLOWED_FILE_TYPES


@app.get("/")
def home() -> dict:
    """A simple message so you know the API is alive."""
    return {"message": "OCR Workbench API is running. Go to /docs to upload a file."}


@app.post("/ocr/local")
async def ocr_local(file: UploadFile = File(...)) -> OCRResult:
    """
    Upload an image or PDF. Runs local OCR and returns the extracted text.
    Also saves the result as a JSON file in the results folder.
    """
    # Check the file type is one we support
    if not file.filename:
        raise HTTPException(status_code=400, detail="No filename provided.")
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

    # Enforce a size limit so we don't process oversized files
    file_size = Path(tmp_path).stat().st_size
    if file_size > MAX_FILE_SIZE_BYTES:
        Path(tmp_path).unlink(missing_ok=True)
        max_mb = MAX_FILE_SIZE_BYTES // (1024 * 1024)
        raise HTTPException(
            status_code=400,
            detail=f"File too large. Max allowed size is {max_mb} MB.",
        )

    try:
        result = run_ocr(tmp_path)
        # Fix the file name in the result to the real uploaded name, not the temp name
        result.file = file.filename
        saved_path = save_result(result)
        result.saved_to = saved_path
        return result
    except FileNotFoundError:
        raise HTTPException(status_code=400, detail="Uploaded file could not be read.")
    except ConfigError:
        # Server misconfiguration — safe to say something is wrong, not what or where
        raise HTTPException(status_code=500, detail="Server is not configured correctly.")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception:
        raise HTTPException(status_code=500, detail="OCR processing failed. Please try again.")
    finally:
        # Clean up the temporary file
        Path(tmp_path).unlink(missing_ok=True)
