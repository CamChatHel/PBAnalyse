"""
Dieses Skript dient zur Erkennung des Messbüros anhand des Logos.
Es wird eine Liste von Bildern übergeben, die das Logo des Messbüros enthalten.
Anschließend wird ein Bildvergleich durchgeführt, um das Messbüro zu identifizieren.
"""

import os
import cv2
import numpy as np
from skimage.metrics import structural_similarity as ssim
import json


# Bildvergleich mit SIFT
def compare_images_sift(img1, img2):
    sift = cv2.SIFT_create()
    kp1, des1 = sift.detectAndCompute(img1, None)
    kp2, des2 = sift.detectAndCompute(img2, None)
    bf = cv2.BFMatcher(cv2.NORM_L2, crossCheck=True)
    matches = bf.match(des1, des2)
    matches = sorted(matches, key=lambda x: x.distance)
    if len(matches) == 0:
        similarity = float('inf')  # Oder ein großer Wert, um anzuzeigen, dass es keine Übereinstimmung gibt
    else:
        similarity = np.sum([m.distance for m in matches]) / len(matches)

    return similarity


# Bildvergleich mit Farbhistogrammen
def compare_images_histogram(img1, img2):
    hist1 = cv2.calcHist([img1], [0, 1, 2], None, [8, 8, 8], [0, 256, 0, 256, 0, 256])
    hist2 = cv2.calcHist([img2], [0, 1, 2], None, [8, 8, 8], [0, 256, 0, 256, 0, 256])
    hist1 = cv2.normalize(hist1, hist1).flatten()
    hist2 = cv2.normalize(hist2, hist2).flatten()
    similarity = cv2.compareHist(hist1, hist2, cv2.HISTCMP_CORREL)
    return similarity


# Bildvergleich mit SSIM
def compare_images_ssim(img1, img2):
    img1_gray = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
    img2_gray = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)

    # Skalierung der Bilder auf gleiche Größe
    img1_resized = cv2.resize(img1_gray, (
    min(img1_gray.shape[1], img2_gray.shape[1]), min(img1_gray.shape[0], img2_gray.shape[0])))
    img2_resized = cv2.resize(img2_gray, (
    min(img1_gray.shape[1], img2_gray.shape[1]), min(img1_gray.shape[0], img2_gray.shape[0])))

    score, _ = ssim(img1_resized, img2_resized, full=True)
    return score


# Kombinierter Bildvergleich
def compare_images_combined(img1, img2):
    sift_similarity = compare_images_sift(img1, img2)
    histogram_similarity = compare_images_histogram(img1, img2)
    ssim_similarity = compare_images_ssim(img1, img2)
    combined_similarity = (sift_similarity + histogram_similarity + ssim_similarity) / 3
    return combined_similarity


# Lese die JSON-Datei und finde den Firmennamen
def get_company_name(image_file, json_path):
    try:
        with open(json_path) as f:
            data = json.load(f)
            for item in data['images']:
                if item['file'] == image_file:
                    return item['company']
    except json.JSONDecodeError as e:
        print(f"Fehler beim Laden der JSON-Datei: {e}")
    return None


#Lese alle Bilddateien aus dem angegebenen Ordner ein
def get_stored_images(folder_path):
    stored_images = []
    for file_name in os.listdir(folder_path):
        if file_name.lower().endswith(('.png', '.jpg', '.jpeg')):
            image_path = os.path.join(folder_path, file_name)
            stored_images.append(image_path)
    return stored_images


# Funktion zur Erkennung des Messbüros über Bildvergleich
def detect_messbuero_via_images(images, stored_images_folder, json_path):
    extracted_images = [np.array(image) for image in images]
    stored_images = get_stored_images(stored_images_folder)

    for extracted_image in extracted_images:
        for stored_image_path in stored_images:
            stored_image = cv2.imread(stored_image_path)
            if stored_image is None:
                if __name__ == "__main__":
                    print(f"Bild konnte nicht geladen werden: {stored_image_path}")
                continue
            similarity = compare_images_combined(extracted_image, stored_image)
            if similarity < 51:  # Schwellenwert für Übereinstimmung
                company_name = get_company_name(os.path.basename(stored_image_path), json_path)
                return company_name

    return None
