"""
HINWEIS:
Um diese Funktion zu nutzen, muss ein API-Key von Mistral AI in der Datei api_key.env hinterlegt sein.
"""

import base64
import requests
import os
from mistralai import Mistral
from dotenv import load_dotenv

def encode_pdf(pdf_path):
    try:
        with open(pdf_path, "rb") as pdf_file:
            return base64.b64encode(pdf_file.read()).decode('utf-8')
    except FileNotFoundError:
        print(f"Error: The file {pdf_path} was not found.")
        return None
    except Exception as e:  # Added general exception handling
        print(f"Error: {e}")
        return None

# Path to your pdf
pdf_path = r"pdf_path"

# Getting the base64 string
base64_pdf = encode_pdf(pdf_path)

load_dotenv(dotenv_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "..", "api_key.env"))
api_key = os.getenv("MISTRAL_API_KEY")

#api_key.env = os.environ["MISTRAL_API_KEY"]
client = Mistral(api_key=api_key)

ocr_response = client.ocr.process(
    model="mistral-ocr-latest",
    document={
        "type": "document_url",
        "document_url": f"data:application/pdf;base64,{base64_pdf}"
    }
)

# Ausgabe als lesbarer Text
for page in ocr_response.pages:
    print(f"\n--- Seite {page.index + 1} ---\n")
    print(page.markdown)