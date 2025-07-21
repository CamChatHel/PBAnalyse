"""
Messart und Parameter
"""

import re
from B_backend.extract.text_in_blocks import extract_blocks
from B_backend.datasets.data import get_messwerte_1_art_data
from B_backend.datasets.info import get_messarten, get_parameter_synonyms, get_ps_id
from B_backend.extract.text_line_by_line import extract_line_by_line


def extract_messart(text,lines):
    data = get_messwerte_1_art_data()
    messarten = get_messarten
    parameter_synonyms = get_parameter_synonyms
    ps_id = get_ps_id()

    # Messart
    found_messart = None
    for messart in messarten:
        for begriff in messart["Begriffe"]:
            if re.search(r"\b" + re.escape(begriff) + r"\b", text):

                data["MESSART"] = messart["Messart"]
                data["M_ID"] = messart["M_ID"]
                found_messart = messart
                break
        if found_messart:
            break

    # Parameter-Suche
    # Falls keine Messart gefunden wurde, alle Parameter aus allen Messarten durchsuchen
    relevant_parameters = {}

    if found_messart:
        relevant_parameters = found_messart["Parameter"]
    else:
        # Falls keine Messart gefunden, alle Parameter aus allen Messarten zusammenführen
        for messart in messarten:
            relevant_parameters.update(messart["Parameter"])

    # Parameter
    for param, beschreibung in relevant_parameters.items():
        if re.search(r"\b" + re.escape(param) + r"\b", "\n".join(lines)):
            data["PARAMETER"] = param
            data["BESCHREIBUNG"] = beschreibung
                # Hinzufügen der PS_ID basierend auf dem Parameter
            if beschreibung in ps_id:
                data["PS_ID"] = ps_id[beschreibung]
            break

    if data.get("PARAMETER") == "-" and data.get("BESCHREIBUNG") == "-":
        for synonym, canonical in parameter_synonyms.items():
            if re.search(r"\b" + re.escape(synonym) + r"\b", "\n".join(lines)):
                if canonical in relevant_parameters:
                    data["PARAMETER"] = canonical
                    data["BESCHREIBUNG"] = relevant_parameters[canonical]
                    # Hinzufügen der PS_ID basierend auf dem Parameter
                    if found_messart["Parameter"][canonical] in ps_id:
                        data["PS_ID"] = ps_id[relevant_parameters[canonical]]
                    break
    if data["MESSART"] == "-":
        data["MESSART"] = "Luftschalldaemmung"
    if data["M_ID"] == "-":
        data["M_ID"] = 1
    return data


# Beispielanwendung
if __name__ == "__main__":
    pdf_path = r"pdf_path"
    text = extract_blocks(pdf_path)
    lines = extract_line_by_line(pdf_path)

    extracted_text = extract_blocks(pdf_path)
    extracted_lines = extract_line_by_line(pdf_path)
    extracted_messart = extract_messart(extracted_text,extracted_lines)
    print(extracted_messart)
