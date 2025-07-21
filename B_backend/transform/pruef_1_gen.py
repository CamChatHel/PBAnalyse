"""
Allgemeine Informationen zur Prüfsituation
"""

import re
from datetime import datetime

from B_backend.extract.text_in_blocks import extract_blocks

from B_backend.datasets.patterns import date_pattern, date_format, messrichtung_pattern
from B_backend.datasets.data import get_pruef_1_gen_data

def build_date_regex(date_patterns):
    regex_parts = []
    for pattern in date_patterns:
        regex_pattern = pattern.replace('%d', r'\d{1,2}') \
                               .replace('%m', r'\d{1,2}') \
                               .replace('%Y', r'\d{4}') \
                               .replace('%y', r'\d{2}') \
                               .replace('%B', r'[A-Za-zäöüÄÖÜß]+\.?') \
                               .replace('%b', r'[A-Za-zäöüÄÖÜß]+\.?')
        regex_parts.append(regex_pattern)
    return r"(" + r"|".join(regex_parts) + r")"

date_regex = build_date_regex(date_format)

def extract_pruef_gen(text):
    data = get_pruef_1_gen_data()

    #  Messdatum
    messdatum_pattern = date_pattern + r"[:\-]?\s*" + date_regex

    messdatum_match = re.search(messdatum_pattern, text, re.IGNORECASE)
    if messdatum_match:
        raw_date = messdatum_match.group(2)
        parsed_date = None

        for pattern in date_format:
            try:
                parsed_date = datetime.strptime(raw_date, pattern).strftime('%d.%m.%Y')
                break
            except ValueError:
                continue

        data["MESSDATUM"] = parsed_date if parsed_date else data["MESSDATUM"]

    #  Messrichtung
    messrichtung_match = re.search(messrichtung_pattern, text, re.IGNORECASE)
    if messrichtung_match:
        for direction in messrichtung_match.groups():
            if direction.lower() in ["horizontal", "horizontale"]:
                data["MESSRICHTUNG"] = "horizontal"
            elif direction.lower() in ["vertikal", "vertikale"]:
                data["MESSRICHTUNG"] = "vertikal"
            elif direction.lower() in ["diagonal", "diagonale", "45°"]:
                data["MESSRICHTUNG"] = "diagonal"
            break
    return data


# Beispielanwendung
if __name__ == "__main__":
    pdf_path = r"pdf_path"
    text = extract_blocks(pdf_path)
    extracted_pruef_gen = extract_pruef_gen (text)
    print(extracted_pruef_gen)
