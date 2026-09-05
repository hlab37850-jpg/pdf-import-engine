#!/bin/bash

echo "🚀 PDF Import Engine Setup"
echo "=============================="
echo ""

if ! command -v python3 &> /dev/null; then
    echo "Python 3 not found"
    exit 1
fi

echo "Creating virtual environment..."
python3 -m venv venv

echo "Activating virtual environment..."
source venv/bin/activate

echo "Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

echo "Creating directories..."
mkdir -p input_files output logs

echo ""
echo "Setup completed!"
echo ""
echo "Next steps:"
echo "1. source venv/bin/activate"
echo "2. python src/main.py <pdf_file>"
echo "3. python -m unittest discover -s tests -p test_*.py -v"
echo ""
