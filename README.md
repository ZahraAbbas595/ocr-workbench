# OCR Workbench

A small learning project that pulls text out of images and PDFs two ways, then compares them:

1. **Local OCR** — using Tesseract (free, open source) on my own computer.
2. **Cloud OCR** — using Azure AI Document Intelligence.

The goal is to learn Git, clean project structure, environment variables and secrets, basic APIs, and how local OCR compares to cloud OCR.

## Project structure

- `local_ocr/` — code that reads text using Tesseract
- `azure_ocr/` — code that reads text using Azure
- `api/` — a small web API to upload a file and get text back
- `samples/` — example images and PDFs to test with
- `results/` — saved OCR results as JSON (ignored by Git)

## Setup

_Steps will be filled in as the project grows._

1. Install Python 3, Tesseract, and Poppler.
2. Create a virtual environment and install the requirements.
3. Copy `.env.example` to `.env` and add your Azure key.

## Status

Project scaffold created. More coming.