import os
import sys
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if project_root not in sys.path:
    sys.path.append(project_root)

os.chdir(project_root)
from config import COMPANY_NAME, JSON_FOLDER

# Text
from B_backend.extract.text_in_blocks import extract_blocks
from B_backend.extract.text_line_by_line import extract_line_by_line
from B_backend.extract.text_tables import extract_table

# Baustelle
from B_backend.transform.baustelle_1_gen import extract_bau
from B_backend.transform.baustelle_2_land import extract_land
from B_backend.transform.sonstiges import extract_sonstiges

# Prüfsituation
from B_backend.transform.pruef_1_gen import extract_pruef_gen
from B_backend.transform.pruef_2_bt import extract_bt, BT_kategorien
from B_backend.transform.ai import pruef_bt_analysis
from B_backend.transform.pruef_3_raum import extract_raum

# Messwerte
from B_backend.transform.messwerte_1_art import extract_messart
from B_backend.transform.messwerte_2_compare import compare_value
from B_backend.transform.messwerte_3_F import extract_measurements

# Plot
from B_backend.transform.plot_graph import create_measurement_graph

# Datasets
from B_backend.datasets.data import get_BT_kategorien
from B_backend.datasets.info import (
    get_bautypen,
    get_messrichtung,
    get_mess_id,
    get_ps_id,
    get_description,
    get_bundeslaender_de,
    get_bundeslaender_oe,
    get_kantone_ch,
    get_land,
    get_messarten,
    get_zustand,
    get_anlass,
    get_raumarten
)

import json

bautypen = get_bautypen
messrichtungen = get_messrichtung
BT_kategorien = get_BT_kategorien ()
messarten = get_mess_id()
parameter = get_description()
ps_id = get_ps_id()
bundeslaender_de = get_bundeslaender_de
bundeslaender_oe = get_bundeslaender_oe
kantone_ch = get_kantone_ch
laender = get_land
bundeslaender = bundeslaender_de + bundeslaender_oe + kantone_ch
mess_para_id = get_messarten
zustaende = get_zustand
anlaesse = get_anlass
raumarten = get_raumarten

def normalize_key(key):
    return key.replace("'","_").replace("°", "deg")

ps_id_normalized = {normalize_key(key): value for key, value in ps_id.items()}
original_keys = {normalize_key(key): key for key in ps_id.keys()}

data_PS_ID = {
    "PS_ID": ps_id_normalized,
    "original_keys": original_keys,
    }

def run_app(pdf_path):
    text = extract_blocks(pdf_path)
    text_lines = extract_line_by_line(pdf_path)
    dfs = extract_table(pdf_path)

    # Baustelle
    baustelle_data = extract_bau(text, pdf_path)
    try:
        with open(COMPANY_NAME, 'r', encoding='utf-8') as file:
            company_data = json.load(file)
        companies = [entry['company'] for entry in company_data['images']]
    except FileNotFoundError:
        companies = []
        if __name__ == "__main__":
            print(f"Warnung: JSON-Datei {COMPANY_NAME} nicht gefunden.")
    except json.JSONDecodeError:
        companies = []
        if __name__ == "__main__":
            print(f"Warnung: Fehler beim Parsen der JSON-Datei {COMPANY_NAME}.")
    land_data = extract_land(text)
    sonstiges_data = extract_sonstiges(text)

    # Pruefsituation
    pruef_gen_data = extract_pruef_gen(text)
    pruef_bt_beschreibung = extract_bt(text)
    pruef_bt_data, pruef_bt_id, pruef_bt_material, pruef_bt_masse, pruef_bt_dicke = pruef_bt_analysis(text)
    pruef_raum_data = extract_raum(text)

    # Messwerte
    messart_data = extract_messart(text, text_lines)
    spectrum_data = compare_value(pdf_path)
    measurement_data = extract_measurements([dfs], pdf_path)

    measurement_graph = create_measurement_graph(measurement_data)

    results = {
        "baustelle_data": baustelle_data,
        "companies": companies,
        "land_data": land_data,
        "sonstiges_data": sonstiges_data,
        "pruef_gen_data": pruef_gen_data,
        "pruef_raum_data": pruef_raum_data,
        "pruef_bt_data": pruef_bt_data,
        "pruef_bt_id": pruef_bt_id,
        "pruef_bt_beschreibung": pruef_bt_beschreibung,
        "pruef_bt_material": pruef_bt_material,
        "pruef_bt_masse": pruef_bt_masse,
        "pruef_bt_dicke": pruef_bt_dicke,

        "messart_data": messart_data,
        "spectrum_data": spectrum_data,
        "measurement_data": measurement_data,
        "measurement_graph": measurement_graph,
        "bautypen": bautypen,
        "messrichtungen": messrichtungen,
        "zustaende": zustaende,
        "anlaesse": anlaesse,
        "BT_kategorien": BT_kategorien,
        "messarten": messarten,
        "parameter": parameter,
        "PS_ID": ps_id,
        "data_PS_ID": data_PS_ID,
        "bundeslaender": bundeslaender,
        "bundeslaender_de": bundeslaender_de,
        "bundeslaender_oe": bundeslaender_oe,
        "kantone_ch": kantone_ch,
        "laender": laender,
        "mess_para_id": mess_para_id,
        "raumarten": raumarten
    }

    temp_folder = os.path.join(JSON_FOLDER, 'temp')
    json_filename = os.path.join(temp_folder, 'cache_results.json')

    with open(json_filename, 'w', encoding='utf-8') as json_file:
        json.dump(results, json_file, indent=4)


    if __name__ == "__main__":
        print(results)

    return results

if __name__ == "__main__":
    pdf_path = r"pdf_path"
    run_app(pdf_path)