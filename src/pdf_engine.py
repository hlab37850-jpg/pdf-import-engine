"""PDF Import Engine - Core Module"""
import os
import json
import logging
from pathlib import Path
from typing import Dict, List, Any, Optional
import pdfplumber
from pdf2image import convert_from_path
import pytesseract
from config.settings import (
    MAX_FILE_SIZE, SUPPORTED_FORMATS, ENCODING,
    TESSERACT_PATH, OUTPUT_FORMAT, EXPORT_DIR, LOG_DIR
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(os.path.join(LOG_DIR, 'pdf_engine.log')),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class PDFImportEngine:
    """High-precision PDF data extraction engine"""
    
    def __init__(self, pdf_path: str):
        """Initialize the engine with a PDF file"""
        self.pdf_path = pdf_path
        self.file_size = None
        self.is_valid = False
        self.extracted_data = {
            'text': [],
            'tables': [],
            'metadata': {}
        }
        logger.info(f"PDFImportEngine initialized with: {pdf_path}")
    
    def validate_pdf(self) -> bool:
        """Validate PDF file format and size"""
        try:
            # Check if file exists
            if not os.path.exists(self.pdf_path):
                logger.error(f"File not found: {self.pdf_path}")
                return False
            
            # Check file extension
            if not any(self.pdf_path.endswith(fmt) for fmt in SUPPORTED_FORMATS):
                logger.error(f"Unsupported file format: {self.pdf_path}")
                return False
            
            # Check file size
            self.file_size = os.path.getsize(self.pdf_path)
            if self.file_size > MAX_FILE_SIZE:
                logger.error(f"File size exceeds limit: {self.file_size} > {MAX_FILE_SIZE}")
                return False
            
            # Validate PDF structure
            with pdfplumber.open(self.pdf_path) as pdf:
                if len(pdf.pages) == 0:
                    logger.error("PDF has no pages")
                    return False
            
            self.is_valid = True
            logger.info(f"PDF validated successfully: {self.pdf_path}")
            return True
        
        except Exception as e:
            logger.error(f"PDF validation failed: {str(e)}")
            return False
    
    def extract_text(self) -> List[str]:
        """Extract text from all PDF pages"""
        if not self.is_valid:
            logger.warning("PDF not validated. Run validate_pdf() first.")
            return []
        
        try:
            texts = []
            with pdfplumber.open(self.pdf_path) as pdf:
                for page_num, page in enumerate(pdf.pages, 1):
                    text = page.extract_text()
                    if text:
                        texts.append({
                            'page': page_num,
                            'content': text.strip()
                        })
            
            self.extracted_data['text'] = texts
            logger.info(f"Extracted text from {len(texts)} pages")
            return texts
        
        except Exception as e:
            logger.error(f"Text extraction failed: {str(e)}")
            return []
    
    def extract_tables(self) -> List[Dict[str, Any]]:
        """Extract tables from PDF"""
        if not self.is_valid:
            logger.warning("PDF not validated. Run validate_pdf() first.")
            return []
        
        try:
            tables = []
            with pdfplumber.open(self.pdf_path) as pdf:
                for page_num, page in enumerate(pdf.pages, 1):
                    page_tables = page.extract_tables()
                    if page_tables:
                        for table_idx, table in enumerate(page_tables, 1):
                            tables.append({
                                'page': page_num,
                                'table_id': table_idx,
                                'data': table
                            })
            
            self.extracted_data['tables'] = tables
            logger.info(f"Extracted {len(tables)} tables from PDF")
            return tables
        
        except Exception as e:
            logger.error(f"Table extraction failed: {str(e)}")
            return []
    
    def extract_metadata(self) -> Dict[str, Any]:
        """Extract PDF metadata"""
        if not self.is_valid:
            logger.warning("PDF not validated. Run validate_pdf() first.")
            return {}
        
        try:
            with pdfplumber.open(self.pdf_path) as pdf:
                metadata = pdf.metadata
                self.extracted_data['metadata'] = {
                    'title': metadata.get('Title', 'N/A'),
                    'author': metadata.get('Author', 'N/A'),
                    'creator': metadata.get('Creator', 'N/A'),
                    'producer': metadata.get('Producer', 'N/A'),
                    'total_pages': len(pdf.pages),
                    'file_size_bytes': self.file_size
                }
            
            logger.info(f"Extracted metadata: {self.extracted_data['metadata']}")
            return self.extracted_data['metadata']
        
        except Exception as e:
            logger.error(f"Metadata extraction failed: {str(e)}")
            return {}
    
    def export_json(self, output_filename: Optional[str] = None) -> str:
        """Export extracted data to JSON"""
        try:
            if not output_filename:
                base_name = Path(self.pdf_path).stem
                output_filename = f"{base_name}_extracted.json"
            
            output_path = os.path.join(EXPORT_DIR, output_filename)
            
            with open(output_path, 'w', encoding=ENCODING) as f:
                json.dump(self.extracted_data, f, indent=2, ensure_ascii=False)
            
            logger.info(f"Data exported to: {output_path}")
            return output_path
        
        except Exception as e:
            logger.error(f"JSON export failed: {str(e)}")
            return ""
    
    def process(self) -> bool:
        """Full processing pipeline"""
        logger.info(f"Starting PDF processing: {self.pdf_path}")
        
        if not self.validate_pdf():
            return False
        
        self.extract_text()
        self.extract_tables()
        self.extract_metadata()
        
        output_path = self.export_json()
        if output_path:
            logger.info(f"Processing completed successfully")
            return True
        
        return False
