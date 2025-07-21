"""
Textextraktion in Textblöcken
"""

import pdfplumber
import tempfile

from B_backend.extract.split_pdf import split_pdf_into_pages

def extract_blocks(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        gesamt_text = ""
        fehlender_text = ""
        for seite in pdf.pages:
            words = seite.extract_words()
            lines = []
            current_line = []

            for word in words:
                word_text = transkriptiere_umlaute(word['text'])
                if current_line and word['x0'] - current_line[-1]['x1'] > 80:
                    fehlender_text += transkriptiere_umlaute(word['text']) + ' '
                else:
                    if current_line and word['top'] > current_line[-1]['top'] + 5:
                        current_line[-1]['text'] += ' \n'
                    current_line.append({'x1': word['x1'], 'text': word_text, 'top': word['top']})

            if current_line:
                lines.append(current_line)

            for line in lines:
                line_text = ' '.join([w['text'] for w in line])
                gesamt_text += line_text + ' '

        text = gesamt_text + "\n" + fehlender_text
        return text

def transkriptiere_umlaute(text):
    replacements = {
        'ä': 'ae',
        'ö': 'oe',
        'ü': 'ue',
        'ß': 'ss',
        'Ä': 'Ae',
        'Ö': 'Oe',
        'Ü': 'Ue',
        '&': 'und'
    }
    for key, value in replacements.items():
        text = text.replace(key, value)
    return text


def process_all_pages(pdf_path):
    with tempfile.TemporaryDirectory() as temp_folder:
        page_paths = split_pdf_into_pages(pdf_path, temp_folder)

        for i, page_pdf in enumerate(page_paths):
            if __name__ == "__main__":
                print(f"\nBericht {i+1}:")
            text = extract_blocks(page_pdf)
            if __name__ == "__main__":
                print(text)


if __name__ == "__main__":
    pdf_path = r"pdf_path"
    process_all_pages(pdf_path)
