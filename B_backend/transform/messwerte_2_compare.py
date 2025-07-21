"""
Vergeleich von messwerte_2_c (Wert aus Text) und messwerte_2_c_berechnung (berechnete Werte)
"""

# Messwerte
from B_backend.transform.messwerte_2_C import extract_spectrum
from B_backend.transform.messwerte_2_C_berechnen import berechnung_anpassung_einzahl
from B_backend.datasets.data import get_messwerte_2_c_berechnet_data

# Text
from B_backend.extract.text_in_blocks import extract_blocks
from B_backend.extract.text_line_by_line import extract_line_by_line
from B_backend.extract.text_tables import extract_table
from B_backend.extract.text_table_anpassung_fallback import extract_table_anpassung

def compare_values_and_report(key, extracted_value, calculated_value):
    if str(extracted_value) != str(calculated_value):
        return f"Bericht: {extracted_value} dB, Berechnung: {calculated_value} dB"
    return calculated_value

def compare_value(pdf_path):
    text = extract_blocks(pdf_path)
    text_lines = extract_line_by_line(pdf_path)
    dfs = extract_table(pdf_path)
    df_2 = extract_table_anpassung(pdf_path)

    # Messwerte
    spectrum_data = extract_spectrum(text_lines, df_2)
    berechnete_data = berechnung_anpassung_einzahl(pdf_path)

    keys_to_compare = get_messwerte_2_c_berechnet_data().keys()

    for key in keys_to_compare:
        berechnete_data[key] = compare_values_and_report(key, spectrum_data[f"{key}_text"], berechnete_data[key])

    return berechnete_data

if __name__ == "__main__":
    pdf_path = r"pdf_path"
    updated_berechnete_data = compare_value(pdf_path)
    print(updated_berechnete_data)

