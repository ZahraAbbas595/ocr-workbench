import os
from datetime import datetime
from pathlib import Path

from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.core.credentials import AzureKeyCredential
from dotenv import load_dotenv

from models import OCRResult

load_dotenv()

ENDPOINT = os.getenv("AZURE_DOC_INTEL_ENDPOINT")
KEY = os.getenv("AZURE_DOC_INTEL_KEY")


def get_client() -> DocumentIntelligenceClient:
    """Build the Azure client using the endpoint and key from .env."""
    if not ENDPOINT or not KEY:
        raise ValueError(
            "Missing Azure credentials. Check that AZURE_DOC_INTEL_ENDPOINT "
            "and AZURE_DOC_INTEL_KEY are set in your .env file."
        )
    return DocumentIntelligenceClient(endpoint=ENDPOINT, credential=AzureKeyCredential(KEY))


def run_azure_ocr(file_path: str) -> OCRResult:
    """
    Send a file to Azure Document Intelligence using the prebuilt "read" model
    (plain OCR, matches what local Tesseract does) and return the extracted text.
    """
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    client = get_client()

    with open(path, "rb") as f:
        poller = client.begin_analyze_document(
            model_id="prebuilt-read",
            body=f,
            content_type="application/octet-stream",
        )
    result = poller.result()

    # Pull the plain text out of Azure's response
    text = result.content if hasattr(result, "content") else ""

    return OCRResult(
        source="azure_document_intelligence",
        file=path.name,
        file_type=path.suffix.lower().replace(".", ""),
        timestamp=datetime.utcnow(),
        text=text.strip(),
    )


def save_azure_result(result: OCRResult, output_dir: str = "results") -> str:
    """Save the Azure OCR result as a JSON file. Returns the path it was saved to."""
    Path(output_dir).mkdir(exist_ok=True)
    timestamp_str = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    filename = f"azure_{Path(result.file).stem}_{timestamp_str}.json"
    output_path = Path(output_dir) / filename
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(result.model_dump_json(indent=2))
    return str(output_path)
