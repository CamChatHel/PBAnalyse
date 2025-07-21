"""
Frequenzabhängige Messwerte aus Tabellenextraktion
"""

import re

from B_backend.extract.text_tables import extract_table
from B_backend.extract.text_table_fallback import extract_table_from_area

from B_backend.datasets.data import get_messwerte_3_f_data


def extract_measurements(dfs, pdf_path):
    data = get_messwerte_3_f_data()

    freq_map = {
        "50": "F0050", "63": "F0063", "80": "F0080", "100": "F0100", "125": "F0125", "160": "F0160",
        "200": "F0200", "250": "F0250", "315": "F0315", "400": "F0400", "500": "F0500", "630": "F0630",
        "800": "F0800", "1000": "F1000", "1250": "F1250", "1600": "F1600", "2000": "F2000",
        "2500": "F2500", "3150": "F3150", "4000": "F4000", "5000": "F5000"
    }
    all_values = []

    for df in dfs:
        for _, row in df.iterrows():
            values = re.findall(r"[\d.,]+", row.iloc[1])
            if values:
                all_values.extend(values)
            freqs = re.findall(r"\d+", row.iloc[0].replace(".", "").replace(" ", ""))
            values = re.findall(r"[\d.,]+", row.iloc[1])

            if len(freqs) == len(values):
                for j, freq in enumerate(freqs):
                    if freq in freq_map:
                        data[freq_map[freq]] = values[j].replace(",", ".")
            else:
                if len(freqs) > 0:
                    freq_list = row.iloc[0].split("\n")
                    val_list = row.iloc[1].split("\n")
                    for j, freq in enumerate(freq_list):
                        clean_freq = freq.replace(".", "").replace(" ", "")
                        if clean_freq in freq_map and j < len(val_list):
                            data[freq_map[clean_freq]] = val_list[j].replace(",", ".")

        number_regex = r"[-+]?\d*[,\.]?\d+"
        if all_values and all(v.strip() == "-" for v in all_values):
            fallback_rows = extract_table_from_area(pdf_path)

            for row in fallback_rows:
                if len(row) != 2 or row[0] is None or row[1] is None:
                    continue
                freq_col = row[0].split("\n")
                value_col = row[1].split("\n")
                for i in range(min(len(freq_col), len(value_col))):
                    freq = freq_col[i].strip()
                    value_raw = value_col[i].strip()
                    match = re.search(number_regex, value_raw)
                    if freq in freq_map:
                        if match:
                            value_clean = float(match.group().replace(",", "."))
                            data[freq_map[freq]] = f"{value_clean:.1f}"
                        else:
                            data[freq_map[freq]] = "0.0"

    return data


# Beispiel zur Verwendung der Funktion
if __name__ == "__main__":
    pdf_path = r"pdf_path"
    dfs = extract_table(pdf_path)
    print(dfs)
    extracted_measurement = extract_measurements([dfs], pdf_path)
    print(extracted_measurement)
