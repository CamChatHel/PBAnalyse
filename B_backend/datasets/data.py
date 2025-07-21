"""
Definition der Datenstrukturen für verschiedene Angaben im Prüfprotokoll.
"""

def get_baustelle_1_gen_data():
    return {
        "MESSBUERO": "-",
        "BAUTYP": "-",
        "BAUJAHR": "-",
        "ZUSTAND": "-",
        "ANLASS": "-"
}

def get_sonstiges_data():
    return {
        "ANMERKUNGEN": "-"
    }

def get_baustelle_2_land_data():
    return {
        "LAND": "-",
        "BUNDESLAND": "-"
    }

def get_messwerte_1_art_data():
    return {
        "MESSART": "-",
        "M_ID": "-",
        "PARAMETER": "-",
        "BESCHREIBUNG": "-",
        "PS_ID": "-"
    }

def get_messwerte_2_c_data():
    return {
        "EINZAHLWERT_text": "-",
        "C_text": "-",
        "C50B3150_text": "-",
        "C50B5000_text": "-",
        "C100B5000_text": "-",
        "CTR_text": "-",
        "CTR50B3150_text": "-",
        "CTR50B5000_text": "-",
        "CTR100B5000_text": "-",
        "CI_text": "-",
        "CI50B2500_text": "-"
    }

def get_messwerte_2_c_berechnet_data():
    return {
        "EINZAHLWERT": "-",
        "C": "-",
        "C50B3150": "-",
        "C50B5000": "-",
        "C100B5000": "-",
        "CTR": "-",
        "CTR50B3150": "-",
        "CTR50B5000": "-",
        "CTR100B5000": "-",
        "CI": "-",
        "CI50B2500": "-"
    }

def get_messwerte_3_f_data():
    return {
        "F0050": "-", "F0063": "-", "F0080": "-", "F0100": "-",
        "F0125": "-", "F0160": "-", "F0200": "-", "F0250": "-",
        "F0315": "-", "F0400": "-", "F0500": "-", "F0630": "-",
        "F0800": "-", "F1000": "-", "F1250": "-", "F1600": "-",
        "F2000": "-", "F2500": "-", "F3150": "-", "F4000": "-",
        "F5000": "-"
    }

def get_pruef_1_gen_data():
    return {
        "MESSDATUM": "-",
        "MESSRICHTUNG": "-"
    }

def get_pruef_2_bt_data():
    return {
        "TRENNBAUTEIL": "-",
        "FLANKE1": "-",
        "FLANKE2": "-",
        "FLANKE3": "-",
        "FLANKE4": "-"
    }

def get_pruef_2_bt_id_data():
   return {
    "TRENNBAUTEIL_ID": "-",
    "FLANKE1_ID": "-",
    "FLANKE2_ID": "-",
    "FLANKE3_ID": "-",
    "FLANKE4_ID": "-"
    }

def get_pruef_2_bt_material_data():
    return {
        "TRENNBAUTEIL_MATERIAL": "-",
        "TRENNBAUTEIL_BAUART": "-",
        "FLANKE1_MATERIAL": "-",
        "FLANKE2_MATERIAL": "-",
        "FLANKE3_MATERIAL": "-",
        "FLANKE4_MATERIAL": "-"
    }

def get_pruef_2_bt_masse_data():
    return {
        "TRENNBAUTEIL_MASSE": "-",
        "FLANKE1_MASSE": "-",
        "FLANKE2_MASSE": "-",
        "FLANKE3_MASSE": "-",
        "FLANKE4_MASSE": "-"
    }

def get_pruef_2_bt_dicke_data():
    return {
        "TRENNBAUTEIL_DICKE": "-",
        "FLANKE1_DICKE": "-",
        "FLANKE2_DICKE": "-",
        "FLANKE3_DICKE": "-",
        "FLANKE4_DICKE": "-"
    }

def get_pruef_2_bt_beschreibung_data():
    return {
        "BT_BESCHREIBUNG_TRENN": "-",
        "BT_BESCHREIBUNG_FLANKEN": "-"
    }


def get_BT_kategorien():
    return {
        "Decke": 1,
        "Wand": 2,
        "Tuer": 3,
        "Fenster": 4,
        "Fussbodenaufbau": 5,
        "Gesamtfassade": 6,
        "Treppenlauf": 7
    }

def get_pruef_3_raum_data():
    return {
        "SENDERAUM": "-",
        "VOLUMENSENDERAUM": "-",
        "EMPFANGSRAUM": "-",
        "VOLUMENEMPFANG": "-",
        "TRENNFLAECHE": "-"
    }

