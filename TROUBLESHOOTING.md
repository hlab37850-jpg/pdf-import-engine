# Troubleshooting Guide

## Common Issues

### 1. Tesseract Not Found
Linux: sudo apt-get install tesseract-ocr
macOS: brew install tesseract
Termux: pkg install tesseract-ocr

### 2. PDF File Not Found
Check file path and permissions

### 3. OCR Processing Slow
OCR is computationally intensive, use --no-ocr if not needed

### 4. Memory Issues
Increase system memory or process smaller PDFs

### 5. Invalid PDF Format
Ensure the file is a valid PDF

### 6. Permission Denied
mkdir -p output
chmod 755 output

### 7. Missing Dependencies
pip install -r requirements.txt

## Getting Help
1. Check this guide
2. Review README.md
3. Check GitHub issues
4. Create new issue with details
