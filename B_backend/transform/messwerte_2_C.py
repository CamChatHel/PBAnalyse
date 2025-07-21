import re
from B_backend.extract.text_line_by_line import extract_line_by_line
from B_backend.datasets.data import get_messwerte_2_c_data
from B_backend.extract.text_table_anpassung_fallback import extract_table_anpassung

def extract_spectrum(lines, table_df):
    data = get_messwerte_2_c_data()

    # Regex für Dezimal- oder Ganzzahlen: -?Ziffern[.(oder,)Ziffern]?
    num = r"-?\d+(?:[.,]\d+)?"

    patterns = {
        "C50B3150_text": [
            rf"C50[ -.,]*3[ .]*1[ .]*50\s*=\s*({num})"
        ],
        "C50B5000_text": [
            rf"C50[ -.,]*5[ .]*000\s*=\s*({num})"
        ],
        "C100B5000_text": [
            rf"C100[ -.,]*5[ .]*000\s*=\s*({num})"
        ],
        "CTR50B3150_text": [
            rf"Ctr[., ]*50[ -.,]*3[ .]*1[ .]*50\s*=\s*({num})"
        ],
        "CTR50B5000_text": [
            rf"Ctr[., ]*50[ -.,]*5[ .]*000\s*=\s*({num})"
        ],
        "CTR100B5000_text": [
            rf"Ctr[., ]*100[ -.,]*5[ .]*000\s*=\s*({num})"
        ],
        "CI_text": [
            rf"(?:CI|\(C\))\s*=\s*({num})(?:\s*\([^)]+\))?\s*dB?"
        ],
        "CI50B2500_text": [
            rf"CI[, -.,]*50[ -.,]*2[ -.,]*500\s*=\s*({num})"
        ]
    }

    # Gleichungsmuster anpassen
    equation_pattern = rf"""
        \(\s*(?:C\s*;\s*Ctr|C\s*;\s*C)\s*\)\s*=\s*({num})\s*
        \(\s*({num})\s*;\s*({num})\s*\)\s*dB
        |
        \(\s*(?:CI|C)\s*\)\s*=\s*({num})\s*
        \(\s*({num})\s*\)\s*dB
    """
    equation_pattern = re.compile(equation_pattern, re.VERBOSE)

    for line in lines:
        # 1. Einzelwerte aus Textzeilen
        for key, pats in patterns.items():
            for pat in pats:
                m = re.search(pat, line)
                if m:
                    raw = m.group(1).replace(',', '.')
                    data[key] = round(float(raw))
        # 2. Gleichungsmuster
        m_eq = equation_pattern.search(line)
        if m_eq:
            if m_eq.group(1) and m_eq.group(2) and m_eq.group(3):
                (m_eq.group(1).replace(',', '.'))
                data["EINZAHLWERT_text"] = round(float(m_eq.group(1).replace(',', '.')))
                data["C_text"]          = round(float(m_eq.group(2).replace(',', '.')))
                data["CTR_text"]        = round(float(m_eq.group(3).replace(',', '.')))
            elif m_eq.group(4) and m_eq.group(5):
                data["EINZAHLWERT_text"] = round(float(m_eq.group(4).replace(',', '.')))
                data["CI_text"]          = round(float(m_eq.group(5).replace(',', '.')))

    # 3. Ergänzung aus Tabelle
    if table_df is not None and not table_df.empty:
        mapping = {
            "C50B3150_text": ("C", "50 - 3150 Hz"),
            "C50B5000_text": ("C", "50 - 5000 Hz"),
            "C100B5000_text": ("C", "100 - 5000 Hz"),
            "CTR50B3150_text": ("Ctr", "50 - 3150 Hz"),
            "CTR50B5000_text": ("Ctr", "50 - 5000 Hz"),
            "CTR100B5000_text": ("Ctr", "100 - 5000 Hz"),
        }
        for key, (identifier, freq_range) in mapping.items():
            if data.get(key) == "-" or data.get(key) is None:
                row = table_df[
                    (table_df["Identifier"].str.lower() == identifier.lower()) &
                    (table_df["Frequenzbereich (Hz)"]
                         .str.replace(" ", "") == freq_range.replace(" ", ""))
                ]
                if not row.empty:
                    # Hier sind es ohnehin ganze Zahlen
                    data[key] = int(row.iloc[0]["Spektrumanpassungswert (dB)"])
    return data


# Beispielaufruf
if __name__ == "__main__":
    pdf_path = r"pdf_path"
    lines = extract_line_by_line(pdf_path)
    print(lines)
    df_2 = extract_table_anpassung(pdf_path)
    result = extract_spectrum(lines, df_2)
    print(result)
