# Claude Assistant Guide for Mail Archives

## Overview
This directory contains Google Takeout mail exports (.mbox files) and extracted PDFs.

## Useful Commands
- `mbox-viewer Sena.mbox` - View mbox file contents (if mbox-viewer is installed)
- `grep -a "Subject:" Sena.mbox | head` - View email subjects
- `python3 -m mailbox Sena.mbox` - Parse mbox with Python's mailbox module

## Working with .mbox Files
- Use standard libraries like Python's `mailbox` module to parse files
- Extract attachments with `email` module
- For large files, process in chunks or use streaming approaches
- Handle different encodings (UTF-8, ISO-8859, etc.) appropriately
- Respect email privacy and security best practices

## PDF Processing
- Use tools like PyPDF2 or pdf-tools if working with the extracted PDFs
- Handle text extraction and metadata appropriately