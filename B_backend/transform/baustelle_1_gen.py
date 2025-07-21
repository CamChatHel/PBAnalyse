"""
Messbüro, Baujahr, Bautyp und Zustand des Gebäudes
"""
from B_backend.extract.text_in_blocks import extract_blocks
import re
import os
import sys
from pdf2image import convert_from_path
import numpy as np
import PIL

from B_backend.datasets.patterns import (messbuero_pattern, messbueros, messbuero_map, baujahr_pattern, massivbau_pattern,
                                         stahlbau_pattern, holzmassivbau_pattern,
                                         holzleichtbau_pattern, rahmenbau_pattern,
                                         fachwerk_pattern, zustand_pattern, anlass_pattern)
from B_backend.datasets.data  import get_baustelle_1_gen_data
from B_backend.transform.messbuero_logo import detect_messbuero_via_images

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if project_root not in sys.path:
    sys.path.append(project_root)
from config import COMPANY_LOGO_FOLDER, COMPANY_NAME

def crop_bottom_quarter(img):
    height = img.shape[0]
    start_row = int(height * 0.75)  # Startpunkt für das untere Viertel
    return img[start_row:, :]


def extract_bau(text, pdf_path):
    data = get_baustelle_1_gen_data()

    stored_images_folder = COMPANY_LOGO_FOLDER
    json_path = COMPANY_NAME

    for dpi in [500, 300, 250]:
        try:
            images = convert_from_path(pdf_path, dpi=dpi)
            if __name__ == "__main__":
                print(f"PDF erfolgreich konvertiert mit dpi={dpi}")
            break
        except PIL.Image.DecompressionBombError:
            if __name__ == "__main__":
                print(f" DPI {dpi} zu hoch, versuche niedrigeren Wert...")
    else:
        if __name__ == "__main__":
            raise RuntimeError("Keine geeignete DPI-Einstellung gefunden.")

    max_width, max_height = 2500, 3500  # Maximale Größe für die Bilder
    scaled_images = []

    for img in images:
        width, height = img.size
        if width > max_width or height > max_height:
            scale_factor = min(max_width / width, max_height / height)
            new_size = (int(width * scale_factor), int(height * scale_factor))
            img = img.resize(new_size, PIL.Image.LANCZOS)
            if __name__ == "__main__":
                print(f"Bild skaliert auf {new_size}")

        scaled_images.append(img)

    if __name__ == "__main__":
        print("PDF wurde in Bilder umgewandelt.")

    cropped_images = [crop_bottom_quarter(np.array(image)) for image in scaled_images]

    # MESSBUERO
    messbuero_match = re.search(messbuero_pattern + r"\s*:\s*([A-Za-z0-9\s&]+)$", text, re.IGNORECASE | re.MULTILINE)
    if messbuero_match:
        data["MESSBUERO"] = messbuero_match.group(2).strip()

    if data["MESSBUERO"] == "-":
        messbuero_match = re.search(messbueros, text, re.IGNORECASE | re.MULTILINE)

        if messbuero_match:
            data["MESSBUERO"] = messbuero_match.group(0).strip()

    if data["MESSBUERO"] in messbuero_map:
        data["MESSBUERO"] = messbuero_map[data["MESSBUERO"]]

    # Führe den Bildvergleich durch, wenn MESSBUERO "-"
    if data["MESSBUERO"] == "-":
        company_name = detect_messbuero_via_images(cropped_images, stored_images_folder, json_path)
        if company_name:
            data["MESSBUERO"] = company_name

    # BAUTYP
    def determine_bautyp(description):
        massivbau_keywords = massivbau_pattern
        stahlbau_keywords = stahlbau_pattern
        holzmassivbau_keywords = holzmassivbau_pattern
        rahmenbau_keywords = rahmenbau_pattern
        fachwerk_keywords = fachwerk_pattern
        holzleichtbau_keywords = holzleichtbau_pattern
        found_keywords = []

        for keyword in massivbau_keywords:
            if re.search(rf"\b{keyword}\b", description, re.IGNORECASE):
                found_keywords.append(keyword)
                return "Massivbau"
        for keyword in stahlbau_keywords:
            if re.search(rf"\b{keyword}\b", description, re.IGNORECASE):
                found_keywords.append(keyword)
                return "Stahlbau"
        for keyword in holzmassivbau_keywords:
            if re.search(rf"\b{keyword}\b", description, re.IGNORECASE):
                found_keywords.append(keyword)
                return "Holzmassivbau"
        for keyword in rahmenbau_keywords:
            if re.search(rf"\b{keyword}\b", description, re.IGNORECASE):
                found_keywords.append(keyword)
                return "Rahmenbau"
        for keyword in fachwerk_keywords:
            if re.search(rf"\b{keyword}\b", description, re.IGNORECASE):
                found_keywords.append(keyword)
                return "Fachwerk"
        for keyword in holzleichtbau_keywords:
            if re.search(rf"\b{keyword}\b", description, re.IGNORECASE):
                found_keywords.append(keyword)
                return "Holzleichtbau"

        return "Andere"


    data["BAUTYP"] = determine_bautyp(text)

    # BAUJAHR
    baujahr_match = re.search(baujahr_pattern, text, re.IGNORECASE)
    if baujahr_match:
        data["BAUJAHR"] = baujahr_match.group(4)

    # Zustand
    zustand_match = re.search(zustand_pattern, text, re.IGNORECASE)
    if zustand_match:
        data["ZUSTAND"] = zustand_match.group(1)
    else:
        data["ZUSTAND"] = "-"

    #  Anlass
    anlass_match = re.search(anlass_pattern, text, re.IGNORECASE)
    if anlass_match:
        data["ANLASS"] = anlass_match.group(1)
    else:
        data["ANLASS"] = "Anderer"

    # Baujahr
    if data["BAUJAHR"] == "-":
        if data["ZUSTAND"] == "Neubau":
            data["BAUJAHR"] = "2023"
    return data

# Beispielanwendung
if __name__ == "__main__":
    pdf_path = r"pdf_path"
    text = extract_blocks(pdf_path)
    extracted_bau = extract_bau(text, pdf_path)
    print(extracted_bau)
