"""
Raumdaten: Senderaum, Empfangsraum, Volumen, Trennfläche
"""

import re

from B_backend.extract.text_in_blocks import extract_blocks
from B_backend.datasets.patterns import senderaum_pattern, empfangraum_pattern, raumart_patterns, vol_pattern, \
    trennflaeche_pattern, flaeche_context_pattern
from B_backend.datasets.data import get_pruef_3_raum_data


def extract_raum(text):
    data = get_pruef_3_raum_data()

    # Muster für Senderaum und Empfangsraum
    sende_pattern = re.compile(senderaum_pattern)
    empfang_pattern = re.compile(empfangraum_pattern)
    volume_regex = re.compile(vol_pattern, re.IGNORECASE)

    volume_keywords_pattern = re.compile(r"(Volumen|V)\s*[:|=]?\s*", re.IGNORECASE)

    # Senderaum
    sende_match = sende_pattern.search(text)
    if sende_match:
        remaining_text = text[sende_match.end():].strip()
        remaining_text = re.sub(r'\s+', ' ', remaining_text)

        # Volumen im Text nach Senderaum
        volume_match = volume_regex.search(remaining_text)
        if volume_match:
            volume = volume_match.group(1)
            if volume in ["-", "/", ""]:
                data["VOLUMENSENDERAUM"] = "-"
            else:
                try:
                    data["VOLUMENSENDERAUM"] = round(float(volume.replace(',', '.')))
                except ValueError:
                    if __name__ == "__main__":
                        print(f"Fehler bei der Konvertierung des Volumens: {volume}")
        else:
            data["VOLUMENSENDERAUM"] = "-"

    if "VOLUMENSENDERAUM" not in data or data["VOLUMENSENDERAUM"] == "-":
        volume_keywords_match = volume_keywords_pattern.search(text)
        if volume_keywords_match:
            sende_match = sende_pattern.search(text[volume_keywords_match.end():])
            if sende_match:
                remaining_text = text[sende_match.end():].strip()
                remaining_text = re.sub(r'\s+', ' ', remaining_text)

                volume_match = volume_regex.search(remaining_text)
                if volume_match:
                    volume = volume_match.group(1)
                    if volume in ["-", "/", ""]:
                        data["VOLUMENSENDERAUM"] = "-"
                    else:
                        try:
                            data["VOLUMENSENDERAUM"] = round(float(volume.replace(',', '.')))
                        except ValueError:
                            if __name__ == "__main__":
                                print(f"Fehler bei der Konvertierung des Volumens: {volume}")
                else:
                    data["VOLUMENSENDERAUM"] = "-"

    # Empfangsraum
    empfang_match = empfang_pattern.search(text)
    if empfang_match:
        remaining_text = text[empfang_match.end():].strip()
        remaining_text = re.sub(r'\s+', ' ', remaining_text)

        volume_match = volume_regex.search(remaining_text)
        if volume_match:
            volume = volume_match.group(1)
            if volume in ["-", "/", ""]:
                data["VOLUMENEMPFANG"] = "-"
            else:
                try:
                    data["VOLUMENEMPFANG"] = round(float(volume.replace(',', '.')))
                except ValueError:
                    if __name__ == "__main__":
                        print(f"Fehler bei der Konvertierung des Volumens: {volume}")
        else:
            data["VOLUMENEMPFANG"] = "-"

    if "VOLUMENEMPFANG" not in data or data["VOLUMENEMPFANG"] == "-":
        volume_keywords_match = volume_keywords_pattern.search(text)
        if volume_keywords_match:
            empfang_match = empfang_pattern.search(text[volume_keywords_match.end():])
            if sende_match:
                remaining_text = text[empfang_match.end():].strip()
                remaining_text = re.sub(r'\s+', ' ', remaining_text)

                volume_match = volume_regex.search(remaining_text)
                if volume_match:
                    volume = volume_match.group(1)
                    if volume in ["-", "/", ""]:
                        data["VOLUMENEMPFANG"] = "-"
                    else:
                        try:
                            data["VOLUMENEMPFANG"] = round(float(volume.replace(',', '.')))
                        except ValueError:
                            if __name__ == "__main__":
                                print(f"Fehler bei der Konvertierung des Volumens: {volume}")
                else:
                    data["VOLUMENEMPFANG"] = "-"

    # Senderaum-Nutzung
    senderaum_match = re.search(senderaum_pattern, text)
    if senderaum_match:
        remaining_text = text[senderaum_match.end():].strip()
        remaining_text = re.sub(r'\s+', ' ', remaining_text)

        words = remaining_text.split()

        for word in words:
            for pattern_group, raum_typ in raumart_patterns:
                for pattern in pattern_group:
                    if re.search(pattern, word, re.IGNORECASE):
                        data["SENDERAUM"] = raum_typ
                        break
                if data["SENDERAUM"] != "-":
                    break
            if data["SENDERAUM"] != "-":
                break

    # Empfangsraum-Nutzung
    empfangsraum_match = re.search(empfangraum_pattern, text)
    if empfangsraum_match:
        remaining_text = text[empfangsraum_match.end():].strip()
        remaining_text = re.sub(r'\s+', ' ', remaining_text)

        words = remaining_text.split()

        for word in words:
            for pattern_group, raum_typ in raumart_patterns:
                for pattern in pattern_group:
                    if re.search(pattern, word, re.IGNORECASE):
                        data["EMPFANGSRAUM"] = raum_typ
                        break
                if data["EMPFANGSRAUM"] != "-":
                    break
            if data["EMPFANGSRAUM"] != "-":
                break

    # Trennfläche
    trennflaeche_match = re.search(trennflaeche_pattern, text, re.IGNORECASE)
    context_match = re.search(flaeche_context_pattern, text, re.IGNORECASE)
    if trennflaeche_match and context_match:
        trennflaeche_value = re.search(r"(\d+([.,]\d+)?)", trennflaeche_match.group(0)).group(1).replace(",", ".")
        trennflaeche_value = format(float(trennflaeche_value), ".2f")
        data["TRENNFLAECHE"] = trennflaeche_value

    # Fehlerhafte Volumenangabe verhindern
    if data["SENDERAUM"] == "Aussenbereich" :
            data["VOLUMENSENDERAUM"] = "-"

    return data


# Beispielanwendung
if __name__ == "__main__":
    pdf_path = r"pdf_path"
    text = extract_blocks(pdf_path)
    extracted_raum = extract_raum(text)
    print(extracted_raum)
