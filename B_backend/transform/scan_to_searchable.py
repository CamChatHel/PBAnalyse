"""
Gescanntes Dokument in durchsuchbare PDF umwandeln
"""

import pytesseract
from pdf2image import convert_from_path
import fitz
import io

def scan_to_searchable_pdf(pdf_path, scanned_pdf_path, dpi=600, lang='deu'):
    images = convert_from_path(pdf_path, dpi=dpi)

    # Erstelle eine neue durchsuchbare PDF
    pdf_writer = fitz.open()

    for i, image in enumerate(images):
        # OCR auf dem Bild ausführen
        text = pytesseract.image_to_string(image, lang=lang)

        # OCR-Daten extrahieren und als durchsuchbaren Text hinzufügen
        ocr_data = pytesseract.image_to_pdf_or_hocr(image, extension='pdf', lang=lang)

        # Das Originalbild als Seite im neuen PDF-Dokument hinzufügen
        img_byte_arr = io.BytesIO()
        image.save(img_byte_arr, format='PNG')
        img_byte_arr = img_byte_arr.getvalue()

        # Erstelle eine neue Seite mit denselben Dimensionen wie das Bild
        img_pdf = fitz.open("pdf", ocr_data)  # OCR-Ausgabe als durchsuchbare Ebene
        pdf_writer.insert_pdf(img_pdf)  # OCR als neue Seite hinzufügen

    # Speichere das durchsuchbare PDF
    pdf_writer.save(scanned_pdf_path)
    pdf_writer.close()

# Beispielaufruf der Funktion
if __name__ == "__main__":
    pdf_path = r"pdf_path"
    scanned_pdf_path = pdf_path.rsplit('.', 1)[0] + '_searchable.pdf'
    scan_to_searchable_pdf(pdf_path, scanned_pdf_path, dpi=300, lang='deu')
    print(f"Durchsuchbare PDF gespeichert unter: {scanned_pdf_path}")
