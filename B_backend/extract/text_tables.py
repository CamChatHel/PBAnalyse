"""
Tabellenextraktion
"""

import pdfplumber
import pandas as pd
import re
import tempfile

from B_backend.extract.split_pdf import split_pdf_into_pages

def extract_table(pdf_path):
    freq_keywords = ["frequenz", "f", "hz", "hertz"]
    level_keywords = ["terz", "db"]

    number_regex = r"[-+]?\d*[,\.]?\d+"

    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            tables = page.extract_tables()
            for table in tables:
                if len(table) > 0:
                    header = [col.lower() if col is not None else '' for col in table[0]]
                    if __name__ == "__main__":
                        print("Header found:", header)

                    if any(freq_keyword in ''.join(header) for freq_keyword in freq_keywords) and \
                            any(level_keyword in ''.join(header) for level_keyword in level_keywords):

                        df = pd.DataFrame(table[1:], columns=table[0])
                        corrected_rows = []

                        for i in range(len(df)):
                            row = df.iloc[i]
                            freqs = row.iloc[0].split("\n") if pd.notnull(row.iloc[0]) else []
                            values = row.iloc[1].split("\n") if pd.notnull(row.iloc[1]) else []

                            if len(values) < len(freqs):
                                if i + 1 < len(df):
                                    next_row_values = df.iloc[i + 1, 1].split("\n") if pd.notnull(df.iloc[i + 1, 1]) else []
                                    values.extend(next_row_values[: len(freqs) - len(values)])
                                    df.iloc[i + 1, 1] = "\n".join(next_row_values[len(freqs) - len(values):])

                            for j in range(len(freqs)):
                                if j < len(values):
                                    # Extrahiere nur die Zahl, wenn sie im richtigen Format ist
                                    matched_value = re.search(number_regex, values[j])
                                    if matched_value:
                                        corrected_rows.append([freqs[j], matched_value.group(0).replace(",",
                                                                                                        ".")])  # Komma in Punkt umwandeln
                                        # Zahl auf Zwei Dezimalstellen runden
                                        corrected_rows[-1][1] = f"{float(corrected_rows[-1][1]):.1f}"
                                    else:
                                        corrected_rows.append([freqs[j], "0"])
                                else:
                                    corrected_rows.append([freqs[j], "0"])

                        df = pd.DataFrame(corrected_rows, columns=["Frequenz (Hz)", "Wert (dB)"])

                        df = df[~((df["Frequenz (Hz)"] == "0") & (df["Wert (dB)"] == "0"))]

                        df.reset_index(drop=True, inplace=True)
                        return df
    return pd.DataFrame()

def process_all_pages(pdf_path):
    with tempfile.TemporaryDirectory() as temp_folder:
        page_paths = split_pdf_into_pages(pdf_path, temp_folder)

        for i, page_pdf in enumerate(page_paths):
            if __name__ == "__main__":
                print(f"\nBericht {i+1}:")
            df = extract_table(page_pdf)
            if __name__ == "__main__":
                print(df)


if __name__ == "__main__":
    pdf_path = r"pdf_path"
    process_all_pages(pdf_path)
