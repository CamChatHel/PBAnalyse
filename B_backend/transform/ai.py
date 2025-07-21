"""
Integration einer API-Referenz von OpenAI, um eine textbasierte Analyse durchzu-
führen. Ziel ist es, das Trennbauteil sowie dessen Flankenbauteile aus der gegebenen
Beschreibung zu kategorisieren, das Material, die Masse und die Dicke zu identifizie-
ren und die Ergebnisse in einer strukturierten Form auszugeben.
"""

import os
import json
from openai import OpenAI
from dotenv import load_dotenv
from B_backend.extract.text_in_blocks import extract_blocks
from B_backend.transform.pruef_2_bt import extract_bt
from B_backend.datasets.info import get_bauteiltypA, get_bauteiltypB
from B_backend.datasets.data import (
    get_BT_kategorien,
    get_pruef_2_bt_data,
    get_pruef_2_bt_material_data,
    get_pruef_2_bt_masse_data,
    get_pruef_2_bt_dicke_data,
    get_pruef_2_bt_id_data,
)


def analyze_BT(text):

    data_kategorien = get_BT_kategorien().keys()
    data_beschreibung = extract_bt(text)
    beschreibung_trennbauteil = data_beschreibung.get("BT_BESCHREIBUNG_TRENN")
    beschreibung_flanken = data_beschreibung.get("BT_BESCHREIBUNG_FLANKEN")

    # API-Key laden
    load_dotenv(dotenv_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "..", "key.env"))
    api_key = os.getenv("API_KEY")
    if api_key is None:
        raise ValueError("API_KEY not found. Make sure it is set in the key.env file.")

    client = OpenAI(api_key=api_key)

    beispiel_beschreibung = (
        "Beschreibung des Trennbauteils:"
        "Wohnungstrenndecke zwischen 2.OG und 1.OG, bestehend aus 20 cm Stahlbeton, 65 mm Ausgleichsschicht, "
        "30 mm Trittschalldämmung (dyn. Steifigkeit: 20 MN/m³) und 70 mm Zementestrich. \n\n"
        "Beschreibung der Flanken: 17,5 cm Mauerwerkswand innen, 17,5 cm gemauerte Fassade mit WDVS "
        "sowie Trockenbauwaende."
    )
    beispiel_antwort = {
        "TRENNBAUTEIL_KATEGORIE": "Decke",
        "TRENNBAUTEIL_MATERIAL": "Stahlbeton",
        "TRENNBAUTEIL_MASSE": "-",
        "TRENNBAUTEIL_DICKE": 20,
        "FLANKE1_KATEGORIE": "Wand",
        "FLANKE1_MATERIAL": "Mauerwerk",
        "FLANKE1_MASSE": "-",
        "FLANKE1_DICKE": 17.5,
        "FLANKE2_KATEGORIE": "Gesamtfassade",
        "FLANKE2_MATERIAL": "Mauerwerk",
        "FLANKE2_MASSE": "-",
        "FLANKE2_DICKE": 17.5,
        "FLANKE3_KATEGORIE": "Wand",
        "FLANKE3_MATERIAL": "Trockenbau",
        "FLANKE3_MASSE": "-",
        "FLANKE3_DICKE": "-",
        "FLANKE4_KATEGORIE": "Wand",
        "FLANKE4_MATERIAL": "Trockenbau",
        "FLANKE4_MASSE": "-",
        "FLANKE4_DICKE": "-"
    }

    context = (
        "Du bist ein Experte im Bauwesen und in der Bauphysik. Deine Aufgabe ist es, eine exakte Analyse zu liefern, "
        "die ausschließlich auf den vorliegenden Informationen basiert. "
        "Die Antwort soll logisch abgeleitete Informationen enthalten, ohne typische Werte zu schätzen. "
        "Hier ist ein Beispiel für eine Beschreibung und die erwartete Antwort:\n\n"
        f"Beispiel-Beschreibung:\n{beispiel_beschreibung}\n\n"
        f"Beispiel-Antwort:\n{json.dumps(beispiel_antwort, indent=2)}\n\n"
        "Falls ein Plural (z.B. 'Waende') in der Beschreibung der Flanken vorkommt, verweist das ggf. auf zwei unterschiedliche Flanken. "
        "Gib die Antwort ohne weitere Erklärungen im JSON-Format zurück."
    )

    anweisung = (
        "Analysiere die Beschreibung und ordne die Bauteile (Trennbauteil und Flanken) den BT_kategorien zu. "
        "Ermittle, falls vorhanden, Material, Masse (in kg/m²) und Dicke (in cm). "
        "Gebe für das Material nur das Hauptmaterial an, z.B. 'Stahlbeton' statt 'Stahlbeton, verputzt'. "
        "Achte darauf, dass du die Beschreibung des Trennbauteils und von den Flanken seperat behandelst. "
        "Falls Informationen fehlen, nutze dein Wissen, um logische Schlussfolgerungen zu ziehen, aber "
        "vermeide es, Annahmen zu treffen, die nicht direkt durch den Text gestützt werden."
    )

    input_data = (
        f"BT_kategorien = {data_kategorien};\n"
        f"Beschreibung des Trennbauteils = {beschreibung_trennbauteil};\n"
        f"Beschreibung der Flanken = {beschreibung_flanken}"
    )

    output_format = (
        "{\n"
        "  \"TRENNBAUTEIL_KATEGORIE\": [Kategorie des Trennbauteils, wenn vorhanden],\n"
        "  \"TRENNBAUTEIL_MATERIAL\": [Material des Trennbauteils, wenn vorhanden],\n"
        "  \"TRENNBAUTEIL_MASSE\": [Zahl in kg/m² für Trennbauteil, wenn vorhanden],\n"
        "  \"TRENNBAUTEIL_DICKE\": [Zahl in cm für Trennbauteil, wenn vorhanden],\n"
        "  \"FLANKE1_KATEGORIE\": [Kategorie der ersten Flanke, wenn vorhanden],\n"
        "  \"FLANKE1_MATERIAL\": [Material der ersten Flanke, wenn vorhanden],\n"
        "  \"FLANKE1_MASSE\": [Zahl in kg/m² für die erste Flanke, wenn vorhanden],\n"
        "  \"FLANKE1_DICKE\": [Zahl in cm für die erste Flanke, wenn vorhanden],\n"
        "  \"FLANKE2_... bis FLANKE4_...\": [Analog zur Struktur der FLANKE1]\n"
        "}\n\n"
    )

    try:
        # Anfrage an die OpenAI API
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": context},
                {"role": "user",
                 "content": f"Anweisung: {anweisung}\n\nInput Data: {input_data}\n\nOutput Data: {output_format}"}
            ],
            temperature=0.5,
            max_tokens=500,
            top_p=0.8,
            frequency_penalty=0,
            presence_penalty=0,
        )

        # Antwort extrahieren
        response_text = response.choices[0].message.content.strip()
        return response_text
    except Exception as e:
        print(f"Fehler bei der Anfrage: {str(e)}")
        return None


def analyze_bt_with_model_response(model_response):
    """
    Funktion zum Verarbeiten der Modellantwort.
    """
    data_bt = get_pruef_2_bt_data()
    data_material = get_pruef_2_bt_material_data()
    data_masse = get_pruef_2_bt_masse_data()
    data_dicke = get_pruef_2_bt_dicke_data()
    data_bt_id = get_pruef_2_bt_id_data()
    data_kategorien = get_BT_kategorien()

    if model_response.startswith("```json") and model_response.endswith("```"):
        model_response = model_response[7:-3]

    try:
        response_data = json.loads(model_response)
    except json.JSONDecodeError:
        print("Fehler: Antwort konnte nicht als JSON geparsed werden.")
        return data_bt, data_bt_id, data_material, data_masse, data_dicke

    for bauteil in ['TRENNBAUTEIL', 'FLANKE1', 'FLANKE2', 'FLANKE3', 'FLANKE4']:
        for attribute in ['KATEGORIE', 'MATERIAL', 'MASSE', 'DICKE']:
            key = f"{bauteil}_{attribute}"
            value = response_data.get(key, "-")

            if attribute == "KATEGORIE" and value in data_kategorien:
                data_bt[bauteil] = value
                data_bt_id[f"{bauteil}_ID"] = data_kategorien.get(value, "-")
            elif attribute == "MATERIAL":
                data_material[f"{bauteil}_MATERIAL"] = value
            elif attribute == "MASSE":
                try:
                    data_masse[f"{bauteil}_MASSE"] = int(round(float(value)))
                except ValueError:
                    data_masse[f"{bauteil}_MASSE"] = "-"

            elif attribute == "DICKE":
                try:
                    dicke_float = float(value)
                    if dicke_float == int(dicke_float):
                        data_dicke[f"{bauteil}_DICKE"] = int(dicke_float)
                    elif len(str(dicke_float).split(".")[1]) > 1:
                        data_dicke[f"{bauteil}_DICKE"] = round(dicke_float, 1)
                    else:
                        data_dicke[f"{bauteil}_DICKE"] = dicke_float
                except ValueError:
                    data_dicke[f"{bauteil}_DICKE"] = "-"

    # Bauteiltyp bestimmen
    bauteiltypA = get_bauteiltypA
    bauteiltypB = get_bauteiltypB

    def determine_trennbauteil_bauart(material):
        if any(word in material.lower() for word in bauteiltypB):
            return "Typ B"
        elif any(word in material.lower() for word in bauteiltypA):
            return "Typ A"
        return "-"

    trennbauteil_material = data_material.get("TRENNBAUTEIL_MATERIAL", "-")
    data_material["TRENNBAUTEIL_BAUART"] = determine_trennbauteil_bauart(trennbauteil_material)

    return data_bt, data_bt_id, data_material, data_masse, data_dicke


def pruef_bt_analysis(text):
    model_response = analyze_BT(text)
    analyzed_data = analyze_bt_with_model_response(model_response)
    return analyzed_data


if __name__ == "__main__":
    # Beispielpfad zum PDF
    pdf_path = r"pdf_path"
    text = extract_blocks(pdf_path)
    analyzed_bt_data = pruef_bt_analysis(text)
    print(analyzed_bt_data)
