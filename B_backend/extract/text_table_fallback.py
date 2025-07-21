import pdfplumber

def extract_table_from_area(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        page = pdf.pages[0]

        # Werte müssen evtl. angepasst werden (je nach PDF-Auflösung)
        left = 0
        top = 100
        right = 180
        bottom = 750

        table_area = page.within_bbox((left, top, right, bottom))
        table = table_area.extract_table()

        return table

if __name__ == "__main__":
    pdf_path = r"pdf_path"
    table = extract_table_from_area(pdf_path)
    print(table)