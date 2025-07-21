import pdfplumber
import pandas as pd
import re
import tempfile

from B_backend.extract.split_pdf import split_pdf_into_pages

def extract_table_anpassung(pdf_path):

    freq_regex = re.compile(r'\d+\s*-\s*\d+\s*Hz', re.IGNORECASE)
    identifier_block_regex = re.compile(r'\b(C|Ctr)\b\s*((?:-?\d+\s*dB\s*)+)', re.IGNORECASE)
    db_value_regex = re.compile(r'-?\d+')

    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text() or ""
            lines = text.splitlines()

            for i, line in enumerate(lines):
                freq_matches = freq_regex.findall(line)
                if freq_matches:
                    # Frequenzbereiche gefunden – suche ab dieser Zeile weiter nach "C", "Ctr" + dB-Blöcken
                    joined_lines = " ".join(lines[i:i+5])  # max 5 Zeilen weiter analysieren

                    data = []
                    blocks = identifier_block_regex.findall(joined_lines)

                    for identifier, db_block in blocks:
                        db_values = db_value_regex.findall(db_block)
                        if len(db_values) == len(freq_matches):
                            for freq, db_val in zip(freq_matches, db_values):
                                data.append({
                                    "Identifier": identifier,
                                    "Frequenzbereich (Hz)": freq.strip(),
                                    "Spektrumanpassungswert (dB)": int(db_val)
                                })

                    if data:
                        return pd.DataFrame(data)

    # Leere Tabelle, wenn nichts gefunden
    return pd.DataFrame(columns=["Identifier", "Frequenzbereich (Hz)", "Spektrumanpassungswert (dB)"])




def process_all_pages(pdf_path):
    with tempfile.TemporaryDirectory() as temp_folder:
        page_paths = split_pdf_into_pages(pdf_path, temp_folder)

        for i, page_pdf in enumerate(page_paths):
            if __name__ == "__main__":
                print(f"\nBericht {i+1}:")
            df = extract_table_anpassung(page_pdf)
            if __name__ == "__main__":
                print(df)

# Beispielanwendung
if __name__ == "__main__":
    pdf_path = r"pdf_path"
    process_all_pages(pdf_path)