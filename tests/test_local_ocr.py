from pathlib import Path

import pytest

from local_ocr.ocr import run_ocr


def test_run_ocr_raises_on_missing_file() -> None:
    with pytest.raises(FileNotFoundError):
        run_ocr("samples/this_file_does_not_exist.pdf")


def test_run_ocr_raises_on_unsupported_file_type(tmp_path: Path) -> None:
    bad_file = tmp_path / "notes.txt"
    bad_file.write_text("just some text")
    with pytest.raises(ValueError):
        run_ocr(str(bad_file))


def test_run_ocr_extracts_text_from_real_pdf() -> None:
    result = run_ocr("samples/sample_text.pdf")
    assert result.source == "local_tesseract"
    assert result.file_type == "pdf"
    assert len(result.text) > 0
