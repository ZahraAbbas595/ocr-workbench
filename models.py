from datetime import datetime

from pydantic import BaseModel, Field


class OCRResult(BaseModel):
    """The result of running OCR on a single file."""

    source: str = Field(
        description="Which engine produced this: local_tesseract or azure_document_intelligence"
    )
    file: str
    file_type: str
    timestamp: datetime
    text: str
    saved_to: str | None = None


class ComparisonStats(BaseModel):
    """Similarity stats between a local and an Azure OCR result."""

    similarity_percent: float
    local_char_count: int
    azure_char_count: int
    diff: list[str]


class ComparisonReport(BaseModel):
    """Full comparison report: both OCR results plus the comparison stats."""

    file: str
    local_result: OCRResult
    azure_result: OCRResult
    comparison: ComparisonStats


class ErrorResponse(BaseModel):
    """A clean, safe error shape returned by the API. Never includes raw internal details."""

    error: str
    detail: str
