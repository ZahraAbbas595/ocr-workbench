# OCR Workbench

A small learning project that extracts text from images and PDFs two ways, then compares the results:

1. **Local OCR** — using Tesseract (free, open source), running entirely on my own computer.
2. **Cloud OCR** — using Azure AI Document Intelligence (Free F0 tier).

Built to practice: Git branches and commits, clean project structure, README-driven development, environment variables and secrets, basic APIs, and comparing local vs cloud OCR.

## Project structure
ocr-workbench/
├── local_ocr/       # Tesseract-based OCR
├── azure_ocr/       # Azure Document Intelligence client
├── api/             # FastAPI upload endpoint
├── samples/         # Test images and PDFs
├── results/         # Saved OCR results as JSON (not committed)
├── compare.py       # Compares local vs Azure OCR output
├── .env.example     # Template for required environment variables
└── requirements.txt

## Setup

### 1. Install prerequisites

**Windows:**
- [Python 3.10+](https://www.python.org/downloads/)
- [Tesseract OCR](https://github.com/UB-Mannheim/tesseract/wiki) — note the install path (usually `C:\Program Files\Tesseract-OCR`)
- [Poppler for Windows](https://github.com/oschwartz10612/poppler-windows/releases) — unzip and note the `Library\bin` path

**macOS:**
```bash
brew install tesseract poppler
```

**Linux (Debian/Ubuntu):**
```bash
sudo apt-get update
sudo apt-get install -y tesseract-ocr poppler-utils
```

On macOS and Linux, both tools install onto your system PATH automatically — no extra path configuration needed.

### 2. Clone and set up the virtual environment

```bash
git clone https://github.com/ZahraAbbas595/ocr-workbench.git
cd ocr-workbench
python -m venv .venv
```

Activate it:
- **Windows:** `.venv\Scripts\activate`
- **macOS/Linux:** `source .venv/bin/activate`

Install dependencies:
```bash
pip install -r requirements.txt
```

### 3. Configure environment variables

```bash
cp .env.example .env
```
(On Windows, use `copy .env.example .env` instead.)

Then edit `.env`:
- **`TESSERACT_PATH` / `POPPLER_PATH`** — only required on Windows. Leave blank on macOS/Linux.
- **`AZURE_DOC_INTEL_ENDPOINT` / `AZURE_DOC_INTEL_KEY`** — required on all platforms. See below.

### 4. Getting an Azure Document Intelligence key

1. Create a free [Azure for Students](https://azure.microsoft.com/en-us/free/students) account (no credit card needed) or a normal Azure free account.
2. In the Azure Portal, create a **Document Intelligence** resource.
3. **Set the pricing tier to Free (F0)** — this gives 500 free pages/month, limited to the first 2 pages per document and 4 MB per file.
4. Copy the Endpoint and Key from the resource's "Keys and Endpoint" page into your `.env` file. Never commit this file.

### 5. Verify the setup

```bash
pytest -v
```
All tests should pass. This confirms Tesseract, Poppler, and your Python environment are wired up correctly (Azure tests are not included here to avoid consuming your free-tier quota on every test run).

### Getting an Azure Document Intelligence key

1. Create a free [Azure for Students](https://azure.microsoft.com/en-us/free/students) account (no credit card needed) or a normal Azure free account.
2. In the Azure Portal, create a **Document Intelligence** resource.
3. **Set the pricing tier to Free (F0)** — this gives 500 free pages/month, limited to the first 2 pages per document.
4. Copy the Endpoint and Key from the resource's "Keys and Endpoint" page into your `.env` file. Never commit this file.

## Running it

**Local OCR only, via terminal:**
python -c "from local_ocr.ocr import run_ocr, save_result; r = run_ocr('samples/yourfile.pdf'); save_result(r)"

**Via the API (upload in browser):**
```bash
uvicorn api.main:app --reload
```
Then open `http://127.0.0.1:8000/docs` and try any of:
- `POST /ocr/local` — local Tesseract OCR
- `POST /ocr/azure` — Azure Document Intelligence OCR
- `POST /ocr/compare` — runs both and returns a comparison report

**Compare local vs Azure on one file:**
python compare.py samples/yourfile.pdf
This prints a similarity score and saves a full comparison report to `results/`.

## What I learned / found

- Azure's Free (F0) tier only processes the **first 2 pages** of any document and caps files at 4 MB — a proof-of-concept limit, not production-ready.
- On the sample file used in this project, Azure's OCR was more accurate on logos and small text than local Tesseract, but only covered a fraction of the document because of the F0 page limit.
- Comparing similarity by raw text match isn't perfectly fair when one engine reads fewer pages than the other — worth remembering when reading the numbers.

## Git workflow used

Each feature was built on its own short-lived branch off `main` and merged in once working, with small commits scoped to one change each:

- `feat/local-ocr` — Tesseract OCR for images/PDFs
- `feat/upload-api` — FastAPI upload endpoint
- `feat/azure-ocr` — Azure Document Intelligence client
- `feat/comparison` — local vs Azure comparison script
- `fix/error-handling` — clean error messages for bad input
- `docs/final-readme` — this file