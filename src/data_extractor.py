"""Advanced Data Extraction Module"""
import logging
from typing import Dict, List, Any
import pdfplumber
from pdf2image import convert_from_path
import pytesseract
from config.settings import TESSERACT_PATH
import re

logger = logging.getLogger(__name__)


class AdvancedDataExtractor:
    """Advanced PDF data extraction with OCR support"""
    
    def __init__(self, pdf_path: str):
        self.pdf_path = pdf_path
        pytesseract.pytesseract.pytesseract_cmd = TESSERACT_PATH
    
    def extract_text_with_positions(self) -> List[Dict[str, Any]]:
        """Extract text with position information"""
        try:
            texts_with_positions = []
            
            with pdfplumber.open(self.pdf_path) as pdf:
                for page_num, page in enumerate(pdf.pages, 1):
                    # Extract words with bbox
                    words = page.extract_words()
                    
                    for word in words:
                        texts_with_positions.append({
                            'page': page_num,
                            'text': word['text'],
                            'x0': word['x0'],
                            'y0': word['y0'],
                            'x1': word['x1'],
                            'y1': word['y1']
                        })
            
            logger.info(f"Extracted {len(texts_with_positions)} words with positions")
            return texts_with_positions
        
        except Exception as e:
            logger.error(f"Text position extraction failed: {str(e)}")
            return []
    
    def extract_text_with_ocr(self, use_ocr: bool = False) -> List[Dict]:
        """Extract text with optional OCR for scanned documents"""
        if not use_ocr:
            return []
        
        try:
            ocr_texts = []
            
            # Convert PDF pages to images
            images = convert_from_path(self.pdf_path)
            
            for page_num, image in enumerate(images, 1):
                # Apply OCR
                text = pytesseract.image_to_string(image, lang='ara+eng')
                
                if text.strip():
                    ocr_texts.append({
                        'page': page_num,
                        'ocr_content': text.strip(),
                        'confidence': 'not_measured'
                    })
            
            logger.info(f"OCR extraction completed for {len(ocr_texts)} pages")
            return ocr_texts
        
        except Exception as e:
            logger.error(f"OCR extraction failed: {str(e)}")
            return []
    
    def extract_links(self) -> List[Dict[str, Any]]:
        """Extract hyperlinks from PDF"""
        try:
            links = []
            
            with pdfplumber.open(self.pdf_path) as pdf:
                for page_num, page in enumerate(pdf.pages, 1):
                    page_links = page.extract_links()
                    
                    for link in page_links:
                        links.append({
                            'page': page_num,
                            'url': link.get('uri', ''),
                            'x0': link['x0'],
                            'y0': link['y0'],
                            'x1': link['x1'],
                            'y1': link['y1']
                        })
            
            logger.info(f"Extracted {len(links)} links from PDF")
            return links
        
        except Exception as e:
            logger.error(f"Link extraction failed: {str(e)}")
            return []
    
    def extract_structured_content(self) -> Dict[str, Any]:
        """Extract structured content (headings, paragraphs, lists)"""
        try:
            structured = {
                'headings': [],
                'paragraphs': [],
                'lists': []
            }
            
            with pdfplumber.open(self.pdf_path) as pdf:
                for page_num, page in enumerate(pdf.pages, 1):
                    text = page.extract_text()
                    
                    if text:
                        lines = text.split('\n')
                        
                        for line in lines:
                            stripped = line.strip()
                            
                            # Simple heuristics for classification
                            if len(stripped) > 0:
                                if stripped.isupper() and len(stripped) < 100:
                                    structured['headings'].append({
                                        'page': page_num,
                                        'content': stripped
                                    })
                                elif stripped.startswith('•') or stripped.startswith('-'):
                                    structured['lists'].append({
                                        'page': page_num,
                                        'content': stripped.lstrip('•-').strip()
                                    })
                                elif len(stripped) > 20:
                                    structured['paragraphs'].append({
                                        'page': page_num,
                                        'content': stripped
                                    })
            
            logger.info(f"Structured content extracted")
            return structured
        
        except Exception as e:
            logger.error(f"Structured content extraction failed: {str(e)}")
            return {'headings': [], 'paragraphs': [], 'lists': []}
