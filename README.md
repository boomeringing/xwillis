# PDF Sniffer

This repository includes a simple web page for extracting text from PDF files. Open `pdf_sniffer.html` in a modern browser, select a PDF file, then click **Extract Text** to see the text from all pages.

The original `xwillis2.htm` portfolio page is untouched.

## Convert extracted text to XLS

Run `python convert_to_xls.py input.txt output.xlsx` to parse business information from a text file and write an Excel spreadsheet. Requires `pandas` and `openpyxl`.
