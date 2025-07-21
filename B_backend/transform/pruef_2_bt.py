import re
from re import match

from B_backend.extract.text_in_blocks import extract_blocks
from B_backend.datasets.patterns import trennbauteil_pattern, flanke_pattern, end_patterns, trennbauteil_end
from B_backend.datasets.data import get_BT_kategorien, get_pruef_2_bt_beschreibung_data

BT_kategorien = get_BT_kategorien()


def extract_bt(text):
    data_beschreibung = get_pruef_2_bt_beschreibung_data()
    matches = []

    # Compile das Endpattern korrekt
    end_pattern = re.compile(trennbauteil_end, re.IGNORECASE)

    for match_obj in re.finditer(trennbauteil_pattern, text, re.IGNORECASE):
        following_text = text[match_obj.end():]

        end_match = end_pattern.search(following_text)
        flanke_match = re.search(flanke_pattern, following_text, re.IGNORECASE)

        # Bestimme den cutoff
        cutoff = len(following_text)
        cutoff_candidates = []
        if end_match:
            cutoff_candidates.append(end_match.start())
        if flanke_match:
            cutoff_candidates.append(flanke_match.start())

        cutoff = min(cutoff_candidates) if cutoff_candidates else len(following_text)

        snippet = following_text[:cutoff].strip()
        snippet = re.sub(r'^[^\w]+', '', snippet)
        snippet = ' '.join(snippet.split())

        if __name__ == "__main__":
            print(f"Extrahierte Beschreibung: {snippet}")

        matches.append(snippet)

    BT_BESCHREIBUNG_TRENN = " - ".join(matches) if matches else "-"
    data_beschreibung["BT_BESCHREIBUNG_TRENN"] = BT_BESCHREIBUNG_TRENN

    # Flanken-Bauteile extrahieren
    flanke_match = re.search(flanke_pattern, text, re.IGNORECASE)

    if flanke_match:
        remaining_text = text[flanke_match.end():]
        end_match = end_pattern.search(remaining_text)

        cutoff = len(remaining_text)
        if end_match:
            cutoff = end_match.start()

        relevant_text = remaining_text[:cutoff].strip()
        relevant_text = re.sub(r'^[^\w]+', '', relevant_text).strip()
        data_beschreibung_flanke = ' '.join(relevant_text.split())

        data_beschreibung["BT_BESCHREIBUNG_FLANKEN"] = data_beschreibung_flanke or "-"
    else:
        data_beschreibung["BT_BESCHREIBUNG_FLANKEN"] = "-"

    return data_beschreibung



# Beispielanwendung
if __name__ == "__main__":
    pdf_path = r"pdf_path"
    text = extract_blocks(pdf_path)
    print(f"Extracted text: {text}")
    extracted_beschreibung = extract_bt(text)
    print(extracted_beschreibung)
