import json
from pathlib import Path

from local_ocr.ocr import run_ocr, save_result


def test_save_result_creates_a_json_file(tmp_path: Path) -> None:
    result = run_ocr("samples/sample_text.pdf")
    saved_path = save_result(result, output_dir=str(tmp_path))

    assert Path(saved_path).exists()
    assert saved_path.endswith(".json")

    with open(saved_path, encoding="utf-8") as f:
        data = json.load(f)

    assert data["source"] == "local_tesseract"
    assert data["text"] == result.text
