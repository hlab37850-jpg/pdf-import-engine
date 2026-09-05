"""Unit Tests for PDF Import Engine"""
import unittest
import os
import sys
import json
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.pdf_engine import PDFImportEngine
from src.validator import DataValidator
from config.settings import EXPORT_DIR, OUTPUT_FORMAT


class TestPDFImportEngine(unittest.TestCase):
    """Test PDFImportEngine class"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.test_pdf_path = "input_files/test.pdf"
        self.engine = PDFImportEngine(self.test_pdf_path)
    
    def test_initialization(self):
        """Test engine initialization"""
        self.assertIsNotNone(self.engine)
        self.assertEqual(self.engine.pdf_path, self.test_pdf_path)
        self.assertFalse(self.engine.is_valid)
    
    def test_validate_nonexistent_file(self):
        """Test validation with non-existent file"""
        invalid_engine = PDFImportEngine("nonexistent.pdf")
        self.assertFalse(invalid_engine.validate_pdf())
    
    def test_extracted_data_structure(self):
        """Test extracted data has correct structure"""
        self.assertIn('text', self.engine.extracted_data)
        self.assertIn('tables', self.engine.extracted_data)
        self.assertIn('metadata', self.engine.extracted_data)


class TestDataValidator(unittest.TestCase):
    """Test DataValidator class"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.validator = DataValidator()
        self.valid_text_data = [
            {'page': 1, 'content': 'Sample text content'},
            {'page': 2, 'content': 'More text here'}
        ]
        self.invalid_text_data = [
            {'page': 1, 'content': ''}
        ]
    
    def test_text_validation_valid(self):
        """Test text validation with valid data"""
        is_valid, errors = self.validator.validate_text_data(self.valid_text_data)
        self.assertTrue(is_valid)
        self.assertEqual(len(errors), 0)
    
    def test_text_validation_invalid(self):
        """Test text validation with invalid data"""
        is_valid, errors = self.validator.validate_text_data(self.invalid_text_data)
        self.assertFalse(is_valid)
        self.assertGreater(len(errors), 0)
    
    def test_metadata_validation_valid(self):
        """Test metadata validation with valid data"""
        valid_metadata = {
            'total_pages': 10,
            'file_size_bytes': 1024000,
            'title': 'Test PDF'
        }
        is_valid, errors = self.validator.validate_metadata(valid_metadata)
        self.assertTrue(is_valid)
    
    def test_metadata_validation_invalid(self):
        """Test metadata validation with invalid data"""
        invalid_metadata = {
            'total_pages': 0,
            'file_size_bytes': -100
        }
        is_valid, errors = self.validator.validate_metadata(invalid_metadata)
        self.assertFalse(is_valid)


if __name__ == '__main__':
    unittest.main()
