# MBOX PDF Extractor

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

A Python utility for extracting PDF attachments from MBOX email archives.

## 📋 Overview

This tool extracts all PDF attachments from MBOX files (such as those exported from Gmail via Google Takeout) and saves them to a specified directory with meaningful filenames.

## ✨ Features

- Extracts PDF attachments from any standard MBOX file
- Properly handles encoded filenames and special characters
- Preserves email context in filenames (date and subject)
- Reports progress for large archives
- Sanitizes filenames for cross-platform compatibility
- Easy to use command-line interface

## 🚀 Usage

```bash
# Basic usage (output to "extracted_pdfs" folder)
python extract_pdfs.py your_mbox_file.mbox

# Specify custom output directory
python extract_pdfs.py your_mbox_file.mbox custom_output_dir
```

## 📦 Requirements

- Python 3.6 or higher
- Standard library modules only (no external dependencies)

## 📊 How It Works

The script:

1. Opens the specified MBOX file
2. Iterates through each email message
3. Examines each message part for PDF attachments (by MIME type or filename)
4. Decodes attachment content and encoded filenames
5. Creates sanitized filenames using email subject and date
6. Saves extracted PDFs to the output directory
7. Provides progress updates and a summary when complete

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🤝 Contributing

Contributions are welcome! Feel free to submit a pull request or open an issue.