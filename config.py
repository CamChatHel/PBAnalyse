import os

# Projektbasisverzeichnis
PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))

# Wichtige Ordner
UPLOAD_FOLDER = os.path.join(PROJECT_ROOT, 'A_frontend/uploads')
JSON_FOLDER = os.path.join(PROJECT_ROOT, 'A_frontend/json')
PROCESSED_FILES = os.path.join(PROJECT_ROOT, 'C_model')
COMPANY_LOGO_FOLDER = os.path.join(PROJECT_ROOT, 'B_backend/transform/company_logo')
COMPANY_NAME = os.path.join(COMPANY_LOGO_FOLDER, 'company_logo_data.json')


