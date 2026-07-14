# Changelog

All notable changes to this project are documented here.

## [Unreleased]

### Added
- Local OCR using Tesseract for images and PDFs, with results saved as JSON.
- FastAPI upload endpoint (`/ocr/local`) with interactive Swagger docs.
- Azure AI Document Intelligence integration (`/ocr/azure`) using the Free (F0) tier.
- Local vs Azure comparison script and endpoint (`/ocr/compare`), reporting a similarity score and diff.
- Pydantic models for all API responses and configuration, replacing raw dictionaries.
- File size, file type, and Azure free-tier page-count safeguards.
- Ruff (lint + format) and mypy (type checking), enforced via GitHub Actions CI on every push and pull request.
- Focused test suite (pytest) covering comparison logic, file validation, error handling, and saved results.
- `.env.example` documenting all required environment variables without exposing secrets.

### Changed
- Switched commit messages to Conventional Commits format (`type(scope): summary`).
- API error responses now return safe, generic messages instead of raw internal error details.

### Fixed
- Removed a private internal document from the full Git history.
- Replaced deprecated `datetime.utcnow()` calls with timezone-aware `datetime.now(UTC)`.

### Security
- Confirmed `.env` is git-ignored throughout development; only `.env.example` with placeholder values is committed.