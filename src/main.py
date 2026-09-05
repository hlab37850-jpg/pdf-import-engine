"""Main Application Entry Point"""
import os
import sys
import argparse
import logging
from pdf_engine import PDFImportEngine
from validator import DataValidator
from data_extractor import AdvancedDataExtractor

logger = logging.getLogger(__name__)


def process_single_pdf(pdf_path: str, use_ocr: bool = False, validate: bool = True) -> bool:
    """Process a single PDF file"""
    print(f"\n{'='*60}")
    print(f"Processing: {pdf_path}")
    print(f"{'='*60}\n")
    
    # Initialize engine
    engine = PDFImportEngine(pdf_path)
    
    # Validate PDF
    if not engine.validate_pdf():
        print("❌ PDF validation failed")
        return False
    
    print("✅ PDF validation passed")
    
    # Extract data
    print("\n📊 Extracting data...")
    engine.extract_text()
    engine.extract_tables()
    engine.extract_metadata()
    
    # Extract advanced data
    extractor = AdvancedDataExtractor(pdf_path)
    advanced_data = {
        'links': extractor.extract_links(),
        'structured_content': extractor.extract_structured_content(),
        'text_with_positions': extractor.extract_text_with_positions()
    }
    
    # Add advanced data to extracted data
    engine.extracted_data['advanced'] = advanced_data
    
    # Optional OCR
    if use_ocr:
        print("\n🔍 Performing OCR extraction...")
        ocr_data = extractor.extract_text_with_ocr(use_ocr=True)
        engine.extracted_data['ocr'] = ocr_data
    
    print("✅ Data extraction completed")
    
    # Validate extracted data
    if validate:
        print("\n✔️ Validating extracted data...")
        validator = DataValidator()
        if validator.validate_complete_extraction(engine.extracted_data):
            print("✅ Data validation passed")
            report = validator.get_report()
            print(f"\n📈 Statistics:")
            print(f"   - Total pages: {report['statistics']['total_pages']}")
            print(f"   - Text pages extracted: {report['statistics']['text_pages_extracted']}")
            print(f"   - Tables extracted: {report['statistics']['tables_extracted']}")
            print(f"   - File size: {report['statistics']['file_size_bytes']} bytes")
        else:
            print("❌ Data validation failed")
            report = validator.get_report()
            print(f"\n⚠️ Errors found:")
            for error in report['errors']:
                print(f"   - {error}")
            return False
    
    # Export to JSON
    print("\n💾 Exporting data to JSON...")
    output_path = engine.export_json()
    if output_path:
        print(f"✅ Data exported to: {output_path}")
    else:
        print("❌ Export failed")
        return False
    
    print(f"\n{'='*60}")
    print("✅ Processing completed successfully!")
    print(f"{'='*60}\n")
    
    return True


def main():
    """Main function"""
    parser = argparse.ArgumentParser(
        description='High-Precision PDF Data Import Engine',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
  python main.py input.pdf
  python main.py input.pdf --ocr
  python main.py input.pdf --no-validate
  python main.py input.pdf --ocr --no-validate
        '''
    )
    
    parser.add_argument('pdf_file', help='Path to PDF file')
    parser.add_argument('--ocr', action='store_true', help='Enable OCR for scanned documents')
    parser.add_argument('--no-validate', action='store_true', help='Skip data validation')
    
    args = parser.parse_args()
    
    # Check if file exists
    if not os.path.exists(args.pdf_file):
        print(f"❌ Error: File '{args.pdf_file}' not found")
        sys.exit(1)
    
    # Process PDF
    success = process_single_pdf(
        args.pdf_file,
        use_ocr=args.ocr,
        validate=not args.no_validate
    )
    
    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()
