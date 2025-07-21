"""
Textextraktion zeilenweise
"""

import pdfplumber
import tempfile

from B_backend.extract.split_pdf import split_pdf_into_pages

def extract_line_by_line(pdf_path):
    text_lines = []
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text(x_tolerance=6, y_tolerance=6)
            if page_text:
                for line in page_text.split('\n'):
                    text_lines.append(line)
    return text_lines

def process_all_pages(pdf_path):
    with tempfile.TemporaryDirectory() as temp_folder:
        page_paths = split_pdf_into_pages(pdf_path, temp_folder)

        for i, page_pdf in enumerate(page_paths):
            if __name__ == "__main__":
                print(f"\nBericht {i+1}:")
            lines = extract_line_by_line(page_pdf)
            if __name__ == "__main__":
                print(lines)


if __name__ == "__main__":
    pdf_path = r"pdf_path"
    process_all_pages(pdf_path)
