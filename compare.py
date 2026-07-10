import difflib
import json
import sys
from pathlib import Path

from local_ocr.ocr import run_ocr as run_local_ocr
from azure_ocr.client import run_azure_ocr


def compare_texts(local_text: str, azure_text: str) -> dict:
    """
    Compare two pieces of text and return simple stats:
    a similarity score and a readable diff.
    """
    matcher = difflib.SequenceMatcher(None, local_text, azure_text)
    similarity = round(matcher.ratio() * 100, 2)

    diff_lines = list(
        difflib.unified_diff(
            local_text.splitlines(),
            azure_text.splitlines(),
            fromfile="local_ocr",
            tofile="azure_ocr",
            lineterm="",
        )
    )

    return {
        "similarity_percent": similarity,
        "local_char_count": len(local_text),
        "azure_char_count": len(azure_text),
        "diff": diff_lines,
    }


def run_comparison(file_path: str) -> dict:
    """Run both OCR engines on the same file and compare the results."""
    print(f"Running local OCR on {file_path} ...")
    local_result = run_local_ocr(file_path)

    print(f"Running Azure OCR on {file_path} ...")
    azure_result = run_azure_ocr(file_path)

    comparison = compare_texts(local_result["text"], azure_result["text"])

    report = {
        "file": Path(file_path).name,
        "local_result": local_result,
        "azure_result": azure_result,
        "comparison": comparison,
    }
    return report


def save_report(report: dict, output_dir: str = "results") -> str:
    """Save the full comparison report as JSON."""
    Path(output_dir).mkdir(exist_ok=True)
    filename = f"comparison_{Path(report['file']).stem}.json"
    output_path = Path(output_dir) / filename
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
    return str(output_path)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python compare.py <path-to-file>")
        sys.exit(1)

    file_path = sys.argv[1]

    try:
        report = run_comparison(file_path)
        saved_path = save_report(report)
    except FileNotFoundError as e:
        print(f"Error: {e}")
        sys.exit(1)
    except ValueError as e:
        print(f"Error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Something went wrong: {e}")
        sys.exit(1)

    print("\n--- SUMMARY ---")
    print(f"Similarity: {report['comparison']['similarity_percent']}%")
    print(f"Local characters extracted: {report['comparison']['local_char_count']}")
    print(f"Azure characters extracted: {report['comparison']['azure_char_count']}")
    print(f"Full report saved to: {saved_path}")