"""Data Validation Module"""
import logging
from typing import Dict, List, Any, Tuple
import json
from pathlib import Path

logger = logging.getLogger(__name__)


class DataValidator:
    """Validate extracted PDF data for accuracy and completeness"""
    
    def __init__(self):
        self.validation_report = {
            'status': 'pending',
            'errors': [],
            'warnings': [],
            'statistics': {}
        }
    
    def validate_text_data(self, text_data: List[Dict]) -> Tuple[bool, List[str]]:
        """Validate extracted text data"""
        errors = []
        
        if not isinstance(text_data, list):
            errors.append("Text data must be a list")
            return False, errors
        
        if len(text_data) == 0:
            errors.append("No text data extracted")
            return False, errors
        
        for item in text_data:
            if 'page' not in item or 'content' not in item:
                errors.append(f"Invalid text item structure: {item}")
            elif not isinstance(item['content'], str) or len(item['content'].strip()) == 0:
                errors.append(f"Empty or invalid content on page {item['page']}")
        
        logger.info(f"Text validation: {len(errors)} errors found")
        return len(errors) == 0, errors
    
    def validate_tables(self, tables_data: List[Dict]) -> Tuple[bool, List[str]]:
        """Validate extracted tables"""
        errors = []
        
        if not isinstance(tables_data, list):
            errors.append("Tables data must be a list")
            return False, errors
        
        for table in tables_data:
            if 'page' not in table or 'data' not in table:
                errors.append(f"Invalid table structure: {table}")
            elif not isinstance(table['data'], list):
                errors.append(f"Table data on page {table['page']} is not a list")
            elif len(table['data']) == 0:
                errors.append(f"Empty table on page {table['page']}")
        
        logger.info(f"Tables validation: {len(errors)} errors found")
        return len(errors) == 0, errors
    
    def validate_metadata(self, metadata: Dict) -> Tuple[bool, List[str]]:
        """Validate extracted metadata"""
        errors = []
        
        required_fields = ['total_pages', 'file_size_bytes']
        for field in required_fields:
            if field not in metadata:
                errors.append(f"Missing required metadata field: {field}")
        
        if metadata.get('total_pages', 0) <= 0:
            errors.append("Invalid total_pages value")
        
        if metadata.get('file_size_bytes', 0) <= 0:
            errors.append("Invalid file_size_bytes value")
        
        logger.info(f"Metadata validation: {len(errors)} errors found")
        return len(errors) == 0, errors
    
    def validate_complete_extraction(self, extracted_data: Dict) -> bool:
        """Validate complete extraction result"""
        self.validation_report['errors'] = []
        self.validation_report['warnings'] = []
        
        # Validate structure
        if 'text' not in extracted_data or 'tables' not in extracted_data or 'metadata' not in extracted_data:
            self.validation_report['errors'].append("Missing required keys in extracted data")
            self.validation_report['status'] = 'failed'
            return False
        
        # Validate each component
        text_valid, text_errors = self.validate_text_data(extracted_data['text'])
        table_valid, table_errors = self.validate_tables(extracted_data['tables'])
        metadata_valid, metadata_errors = self.validate_metadata(extracted_data['metadata'])
        
        self.validation_report['errors'].extend(text_errors)
        self.validation_report['errors'].extend(table_errors)
        self.validation_report['errors'].extend(metadata_errors)
        
        # Statistics
        self.validation_report['statistics'] = {
            'total_pages': extracted_data['metadata'].get('total_pages', 0),
            'text_pages_extracted': len(extracted_data['text']),
            'tables_extracted': len(extracted_data['tables']),
            'file_size_bytes': extracted_data['metadata'].get('file_size_bytes', 0)
        }
        
        all_valid = text_valid and table_valid and metadata_valid and len(self.validation_report['errors']) == 0
        self.validation_report['status'] = 'passed' if all_valid else 'failed'
        
        logger.info(f"Complete validation status: {self.validation_report['status']}")
        return all_valid
    
    def get_report(self) -> Dict[str, Any]:
        """Get validation report"""
        return self.validation_report
