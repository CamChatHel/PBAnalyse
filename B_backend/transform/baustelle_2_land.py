"""
Land, Bundesland/Kanton
"""

import re
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut

from B_backend.extract.text_in_blocks import extract_blocks

from B_backend.datasets.patterns import adress_pattern
from B_backend.datasets.data import get_baustelle_2_land_data
from B_backend.datasets.info import get_bundeslaender_de, get_bundeslaender_oe, get_kantone_ch

def extract_land(text):
    data = get_baustelle_2_land_data()

    bundeslaender_de = get_bundeslaender_de
    buendeslaender_oe = get_bundeslaender_oe
    kantone_ch = get_kantone_ch

    bundeslaender = bundeslaender_de + buendeslaender_oe + kantone_ch

    # Muster für Adresslinien
    address_lines = []
    for line in text.splitlines():
        if re.search(r"\b" + adress_pattern + r"\b", line, re.IGNORECASE):
            address_part = line.split(":", 1)[-1].strip()
            address_lines.append(address_part)

    # Füge die gefundenen Adressteile zusammen
    full_address = ", ".join(address_lines)

    # Bereinige Adresse für das Geocoding: Suche PLZ und Stadt
    address_text = re.search(r"\b([A-Za-z\s]+,\s*\d{5}\s+[A-Za-zäöüÄÖÜß]+)", full_address)
    if address_text:
        address_text = address_text.group(1)
    else:
        address_text = full_address

    if __name__ == "__main__":
        print(f"Bereinigte Adresse zum Geocoding: {address_text}")

    # Geolocator initialisieren
    geolocator = Nominatim(user_agent="pdf_extractor", timeout=10)

    try:
        location = geolocator.geocode(address_text, country_codes='de,at,ch', language='de',addressdetails=True)
    except GeocoderTimedOut:
        location = None

    # Falls die vollständige Adresse nicht gefunden wurde, versuche nur Stadt und PLZ
    if not location:
        plz_city_match = re.search(r"\b\d{5}\b\s+([A-Za-zäöüÄÖÜß]+)", full_address)
        if plz_city_match:
            simplified_address = plz_city_match.group(0)
            if __name__ == "__main__":
                print(f"Alternative Adresse zum Geocoding: {simplified_address}")
            try:
                location = geolocator.geocode(simplified_address)
            except GeocoderTimedOut:
                location = None

    if location:
        if __name__ == "__main__":
            print(f"Gefundener Ort: {location.address}")

        # Direkt aus den strukturierten Geocoding-Daten das Bundesland extrahieren
        if 'address' in location.raw:
            address_info = location.raw['address']
            state = address_info.get('state')
            country = address_info.get('country')
            if state:
                data["BUNDESLAND"] = state
            # Hier ordnest du das Land nur den drei möglichen Ländern zu
            if country:
                if "Germany" in country or "Deutschland" in country:
                    data["LAND"] = "Deutschland"
                elif "Austria" in country or "Österreich" in country:
                    data["LAND"] = "Österreich"
                elif "Switzerland" in country or "Schweiz" in country:
                    data["LAND"] = "Schweiz"
        else:
            address_string = location.address
            address_parts = address_string.split(", ")

            for part in address_parts:
                if part in bundeslaender_de:
                    data["BUNDESLAND"] = part
                if "Deutschland" in part or "Germany" in part:
                    data["LAND"] = "Deutschland"
                if part in buendeslaender_oe:
                    data["BUNDESLAND"] = part
                if "Österreich" in part or "Austria" in part:
                    data["LAND"] = "Österreich"
                if part in kantone_ch:
                    data["BUNDESLAND"] = part
                if "Schweiz" in part or "Switzerland" in part:
                    data["LAND"] = "Schweiz"

    # Falls Geocoding nicht erfolgreich ist, suche BUNDESLAND direkt im Text
    if data["BUNDESLAND"] == "-":
        for bundesland in bundeslaender:
            if re.search(rf"\b{bundesland}\b", text, re.IGNORECASE):
                data["BUNDESLAND"] = bundesland
                break

    # Falls Geocoding nicht erfolgreich ist, suche LAND direkt im Text
    if data["LAND"] == "-":
        if "Deutschland" in text:
            data["LAND"] = "Deutschland"
        elif "Germany" in text:
            data["LAND"] = "Deutschland"
        elif "Österreich" in text:
            data["LAND"] = "Österreich"
        elif "Austria" in text:
            data["LAND"] = "Österreich"
        elif "Schweiz" in text:
            data["LAND"] = "Schweiz"
        elif "Switzerland" in text:
            data["LAND"] = "Schweiz"

    return data


# Beispielanwendung
if __name__ == "__main__":
    pdf_path = r"pdf_path"
    text = extract_blocks(pdf_path)
    extracted_land = extract_land(text)
    print(extracted_land)
