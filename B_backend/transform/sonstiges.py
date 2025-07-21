"""
Sonstige Anmerkungen
"""

import re

from B_backend.extract.text_in_blocks import extract_blocks

from B_backend.datasets.patterns import else_pattern, end_patterns
from B_backend.datasets.data import get_sonstiges_data

def extract_sonstiges(text):
    data = get_sonstiges_data()

    # ANMERKUNGEN
    else_match = re.search(else_pattern, text, re.IGNORECASE)

    if else_match:
        following_text = text[else_match.end():]

        end_match = re.search(
            r'\b(' + end_patterns + r')\b|\r?\n',
            following_text,
            re.IGNORECASE
        )
        if end_match:
            following_text = following_text[:end_match.start()].strip()
        else:
            following_text = following_text.strip()

        # Entferne Symbole am Anfang
        following_text = re.sub(r'^[^\w]+', '', following_text).strip()
        data["ANMERKUNGEN"] = ' '.join(following_text.split())
        if data["ANMERKUNGEN"] in ["keine", "nichts", "/", ""]:
            data["ANMERKUNGEN"] = "-"

    return data

# Beispielanwendung
if __name__ == "__main__":
    pdf_path = r"pdf_path"
    text = extract_blocks(pdf_path)
    extracted_sonstiges = extract_sonstiges(text)
    print(extracted_sonstiges)