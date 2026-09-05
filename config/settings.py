"""Configuration settings for PDF Import Engine"""
import os

# File size constraints
MAX_FILE_SIZE = 50 * 1024 * 1024  # 50 MB

# Supported formats
SUPPORTED_FORMATS = ['.pdf']

# Encoding
ENCODING = 'utf-8'

# Tesseract path (for Termux)
TESSERACT_PATH = '/data/data/com.termux/files/usr/bin/tesseract'

# Output settings
OUTPUT_FORMAT = 'json'
EXPORT_DIR = 'output/'
LOG_DIR = 'logs/'

# Create directories if they don't exist
os.makedirs(EXPORT_DIR, exist_ok=True)
os.makedirs(LOG_DIR, exist_ok=True)
