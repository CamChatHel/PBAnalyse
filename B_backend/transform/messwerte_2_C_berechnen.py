"""
Berechnung des Einzahlswertes und der Spektrumanpassungswerte
"""

import math
from B_backend.extract.text_in_blocks import extract_blocks
from B_backend.extract.text_line_by_line import extract_line_by_line
from B_backend.extract.text_table_anpassung_fallback import extract_table_anpassung
from B_backend.datasets.data import get_messwerte_2_c_berechnet_data
from B_backend.extract.text_tables import extract_table
from B_backend.transform.messwerte_2_C import extract_spectrum
from B_backend.transform.messwerte_3_F import extract_measurements
from B_backend.transform.messwerte_1_art import extract_messart

# Schallpegel der Frequenzen für Spektren
BEZUGSKURVE_LUFTSCHALL = [33, 36, 39, 42, 45, 48, 51, 52, 53, 54, 55, 56, 56, 56, 56, 56]
BEZUGSKURVE_TRITTSCHALL = [62, 62, 62, 62, 62, 62, 61, 60, 59, 58, 57, 54, 51, 48, 45, 42]

LI_SPEKTRUM_C = [-29, -26, -23, -21, -19, -17, -15, -13, -12, -11, -10, -9, -9, -9, -9, -9]
LI_SPEKTRUM_C50_3150 = [-40, -36, -33, -29, -26, -23, -21, -19, -17, -15, -13, -12, -11, -10, -9, -9, -9, -9, -9]
LI_SPEKTRUM_C50_5000 = [-41, -37, -34, -30, -27, -24, -22, -20, -18, -16, -14, -13, -12, -11, -10, -10, -10, -10, -10, -10, -10]
LI_SPEKTRUM_C100_5000 = [-30, -27, -24, -22, -20, -18, -16, -14, -13, -12, -11, -10, -10, -10, -10, -10, -10, -10]
LI_SPEKTRUM_CTR = [-20, -20, -18, -16, -15, -14, -13, -12, -11, -9, -8, -9, -10, -11, -13, -15]
LI_SPEKTRUM_CTR50_3150 = [-25, -23, -21, -20, -20, -18, -16, -15, -14, -13, -12, -11, -9, -8, -9, -10, -11, -13, -15]
LI_SPEKTRUM_CTR50_5000 = [-25, -23, -21, -20, -20, -18, -16, -15, -14, -13, -12, -11, -9, -8, -9, -10, -11, -13, -15, -16, -18]
LI_SPEKTRUM_CTR100_5000 = [-20, -20, -18, -16, -15, -14, -13, -12, -11, -9, -8, -9, -10, -11, -13, -15, -16, -18]

import math

def round_half_up(x):
    # Für positive wie negative Werte:
    return math.floor(x + 0.5) if x >= 0 else math.ceil(x - 0.5)

def formel_anpassungswert_luftschall(li, xi, xw):
    sum_term = sum(10 ** ((Li - xi_i) / 10) for Li, xi_i in zip(li, xi))
    cj = -10 * math.log10(sum_term) - xw
    return round_half_up(cj)

def formel_anpassungswert_trittschall(fi, xw):
    sum_term = sum(10 ** (Fi / 10) for Fi in fi)
    ci = 10 * math.log10(sum_term) - 15 - xw
    return round_half_up(ci)


def berechne_einzahlwert_luftschall(bezugskurve_luftschall, messwerte):
    maximale_summe = float('-inf')
    optimale_verschiebung = 0

    for verschiebung in range(-100, 101):
        # Verschieben der Bezugskurve
        verschobene_bezugskurve = [li + verschiebung for li in bezugskurve_luftschall]

        # Berechnung der Summe der positiven Differenzen
        differenz_summe = sum((li - fi) for li, fi in zip(verschobene_bezugskurve, messwerte) if (li - fi) > 0)

        # Überprüfen, ob die Differenzsumme den Bedingungen entspricht
        if differenz_summe <= 32 and differenz_summe > maximale_summe:
            maximale_summe = differenz_summe
            optimale_verschiebung = verschiebung

    return round_half_up(bezugskurve_luftschall[7] + optimale_verschiebung)

def berechne_einzahlwert_trittschall(bezugskurve_trittschall, messwerte):
    maximale_summe = float('-inf')
    optimale_verschiebung = 0

    for verschiebung in range(-100, 101, 1):
        # Verschieben der Bezugskurve
        verschobene_bezugskurve = [li + verschiebung for li in bezugskurve_trittschall]

        # Berechnung der Summe der positiven Differenzen
        differenz_summe = sum((fi - li) for li, fi in zip(verschobene_bezugskurve, messwerte) if (fi - li) > 0)

        # Überprüfen, ob die Differenzsumme den Bedingungen entspricht
        if differenz_summe <= 32 and differenz_summe > maximale_summe:
            maximale_summe = differenz_summe
            optimale_verschiebung = verschiebung

    return round_half_up(bezugskurve_trittschall[7] + optimale_verschiebung)


def get_messwerte_for_spectrum(spectrum, extracted_measurement):
    if spectrum == 'C':
        return [float(extracted_measurement[key]) for key in ["F0100", "F0125", "F0160", "F0200", "F0250", "F0315", "F0400", "F0500", "F0630", "F0800", "F1000", "F1250", "F1600", "F2000", "F2500", "F3150"]]
    elif spectrum == 'C50_3150':
        return [float(extracted_measurement[key]) for key in ["F0050", "F0063", "F0080", "F0100", "F0125", "F0160", "F0200", "F0250", "F0315", "F0400", "F0500", "F0630", "F0800", "F1000", "F1250", "F1600", "F2000", "F2500", "F3150"]]
    elif spectrum == 'C50_5000':
        return [float(extracted_measurement[key]) for key in ["F0050", "F0063", "F0080", "F0100", "F0125", "F0160", "F0200", "F0250", "F0315", "F0400", "F0500", "F0630", "F0800", "F1000", "F1250", "F1600", "F2000", "F2500", "F3150", "F4000", "F5000"]]
    elif spectrum == 'C100_5000':
        return [float(extracted_measurement[key]) for key in ["F0100", "F0125", "F0160", "F0200", "F0250", "F0315", "F0400", "F0500", "F0630", "F0800", "F1000", "F1250", "F1600", "F2000", "F2500", "F3150", "F4000", "F5000"]]
    elif spectrum == 'CTR':
        return [float(extracted_measurement[key]) for key in ["F0100", "F0125", "F0160", "F0200", "F0250", "F0315", "F0400", "F0500", "F0630", "F0800", "F1000", "F1250", "F1600", "F2000", "F2500", "F3150"]]
    elif spectrum == 'CTR50_3150':
        return [float(extracted_measurement[key]) for key in ["F0050", "F0063", "F0080", "F0100", "F0125", "F0160", "F0200", "F0250", "F0315", "F0400", "F0500", "F0630", "F0800", "F1000", "F1250", "F1600", "F2000", "F2500", "F3150"]]
    elif spectrum == 'CTR50_5000':
        return [float(extracted_measurement[key]) for key in ["F0050", "F0063", "F0080", "F0100", "F0125", "F0160", "F0200", "F0250", "F0315", "F0400", "F0500", "F0630", "F0800", "F1000", "F1250", "F1600", "F2000", "F2500", "F3150", "F4000", "F5000"]]
    elif spectrum == 'CTR100_5000':
        return [float(extracted_measurement[key]) for key in ["F0100", "F0125", "F0160", "F0200", "F0250", "F0315", "F0400", "F0500", "F0630", "F0800", "F1000", "F1250", "F1600", "F2000", "F2500", "F3150", "F4000", "F5000"]]
    elif spectrum =='CI':
        return [float(extracted_measurement[key]) for key in ["F0100", "F0125", "F0160", "F0200", "F0250", "F0315", "F0400", "F0500", "F0630", "F0800", "F1000", "F1250", "F1600", "F2000", "F2500"]]
    elif spectrum == 'CI50_2500':
        return [float(extracted_measurement[key]) for key in ["F0050", "F0063", "F0080", "F0100", "F0125", "F0160", "F0200", "F0250", "F0315", "F0400", "F0500", "F0630", "F0800", "F1000", "F1250", "F1600", "F2000", "F2500"]]
    return []

def berechnung_anpassung_einzahl(pdf_path):
    text = extract_blocks(pdf_path)
    lines = extract_line_by_line(pdf_path)
    dfs = extract_table(pdf_path)
    df_2 = extract_table_anpassung(pdf_path)

    extracted_spectrum = extract_spectrum(lines, df_2)
    extracted_measurement = extract_measurements([dfs], pdf_path)
    for key, value in extracted_measurement.items():
        if value == "-":
            extracted_measurement[key] = "0"

    berechnete_data = get_messwerte_2_c_berechnet_data()

    extracted_messart = extract_messart(text, lines)
    m_id = extracted_messart["M_ID"]

    messwerte = get_messwerte_for_spectrum('C', extracted_measurement)

    if m_id == 2:
        xw = berechne_einzahlwert_trittschall(BEZUGSKURVE_TRITTSCHALL, messwerte)

        CI_berechnet = formel_anpassungswert_trittschall(get_messwerte_for_spectrum('CI', extracted_measurement), xw)
        CI50B2500_berechnet = formel_anpassungswert_trittschall(get_messwerte_for_spectrum('CI50_2500', extracted_measurement), xw)
        for key in berechnete_data:
            if key == "EINZAHLWERT":
                berechnete_data[key] = xw
            elif key == "CI":
                berechnete_data[key] = CI_berechnet
            elif key == "CI50B2500":
                berechnete_data[key] = CI50B2500_berechnet


    elif m_id == 3 or m_id == 4 or m_id == 1:
        xw =  berechne_einzahlwert_luftschall(BEZUGSKURVE_LUFTSCHALL, messwerte)
        C_berechnet = formel_anpassungswert_luftschall(LI_SPEKTRUM_C, get_messwerte_for_spectrum('C', extracted_measurement), xw)
        C50B3150_berechnet = formel_anpassungswert_luftschall(LI_SPEKTRUM_C50_3150, get_messwerte_for_spectrum('C50_3150', extracted_measurement), xw)
        C50B5000_berechnet = formel_anpassungswert_luftschall(LI_SPEKTRUM_C50_5000, get_messwerte_for_spectrum('C50_5000', extracted_measurement), xw)
        C100B5000_berechnet = formel_anpassungswert_luftschall(LI_SPEKTRUM_C100_5000, get_messwerte_for_spectrum('C100_5000', extracted_measurement), xw)
        CTR_berechnet = formel_anpassungswert_luftschall(LI_SPEKTRUM_CTR, get_messwerte_for_spectrum('CTR', extracted_measurement), xw)
        CTR50B3150_berechnet = formel_anpassungswert_luftschall(LI_SPEKTRUM_CTR50_3150, get_messwerte_for_spectrum('CTR50_3150', extracted_measurement), xw)
        CTR50B5000_berechnet = formel_anpassungswert_luftschall(LI_SPEKTRUM_CTR50_5000, get_messwerte_for_spectrum('CTR50_5000', extracted_measurement), xw)
        CTR100B5000_berechnet = formel_anpassungswert_luftschall(LI_SPEKTRUM_CTR100_5000, get_messwerte_for_spectrum('CTR100_5000', extracted_measurement), xw)

        for key in berechnete_data:
            if key == "EINZAHLWERT":
                berechnete_data[key] = xw
            elif key == "C":
                berechnete_data[key] = C_berechnet
            elif key == "C50B3150":
                berechnete_data[key] = C50B3150_berechnet
            elif key == "C50B5000":
                berechnete_data[key] = C50B5000_berechnet
            elif key == "C100B5000":
                berechnete_data[key] = C100B5000_berechnet
            elif key == "CTR":
                berechnete_data[key] = CTR_berechnet
            elif key == "CTR50B3150":
                berechnete_data[key] = CTR50B3150_berechnet
            elif key == "CTR50B5000":
                berechnete_data[key] = CTR50B5000_berechnet
            elif key == "CTR100B5000":
                berechnete_data[key] = CTR100B5000_berechnet


    return berechnete_data


if __name__ == "__main__":
    # Beispiel zur Verwendung der Funktionen
    pdf_path = r"pdf_path"
    berechnete_anpassungswerte = berechnung_anpassung_einzahl(pdf_path)
    print(berechnete_anpassungswerte)
