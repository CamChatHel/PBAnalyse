from flask import Flask, request, render_template, redirect, url_for, session, jsonify
from flask_session import Session
from werkzeug.utils import secure_filename
import os
import sys
import json
import tempfile
from datetime import datetime
import copy

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

if project_root not in sys.path:
    sys.path.append(project_root)

os.chdir(project_root)
from B_backend.transform.main import run_app
from B_backend.datasets.labels import labels
from B_backend.extract.excel_to_pdf import excel_to_pdf
from B_backend.transform.scan_to_searchable import scan_to_searchable_pdf
from B_backend.extract.split_pdf import split_pdf_into_pages
from B_backend.transform.plot_graph import create_measurement_graph
from structure_data import structured_data
from config import JSON_FOLDER, COMPANY_LOGO_FOLDER


ALLOWED_EXTENSIONS = {'pdf', 'xlsx', 'xls'}

app = Flask(__name__)
app.secret_key = os.environ.get('WEB_KEY', 'default_secret_key')

# Server-seitige Session-Konfiguration
app.config['SESSION_TYPE']       = 'filesystem'
app.config['SESSION_FILE_DIR']   = '/tmp/flask_session'
app.config['SESSION_PERMANENT']  = False                  # Session endet mit Browser-Schluss
app.config['SESSION_USE_SIGNER'] = True                   # signiert die Cookies

# Extension initialisieren
Session(app)

app.config['JSON_FOLDER'] = JSON_FOLDER
app.config['COMPANY_LOGO_FOLDER'] = COMPANY_LOGO_FOLDER

def finalize_and_cleanup():
    # 1. Werte aus Session
    is_onesite    = session.get('is_onesite', False)
    all_data      = session.get('all_data', [])
    deleted_pages = set(session.get('deleted_pages', []))
    page_paths    = session.get('page_paths', [])

    # 2. Gefilterte Daten (ohne gelöschte und None)
    filtered = [
        data for idx, data in enumerate(all_data)
        if idx not in deleted_pages and data is not None
    ]

    saved_count = len(filtered)
    deleted_count = len(deleted_pages)

    # 3. JSON-Export
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    if not os.path.exists(app.config['JSON_FOLDER']):
        os.makedirs(app.config['JSON_FOLDER'])

    if is_onesite:
        full = {}
        for i, page in enumerate(filtered):
            struct = structured_data(page, is_onesite=True,
                                     is_first_page=(i==0))
            if i == 0:
                full.update(struct)
            else:
                full[f"measurement_{i+1}"] = struct["measurement"]

        fname = os.path.join(app.config['JSON_FOLDER'],
                             f"data_{timestamp}.json")
        with open(fname, 'w', encoding='utf-8') as f:
            json.dump(full, f, ensure_ascii=False, indent=4)
    else:
        for i, page in enumerate(filtered, start=1):
            struct = structured_data(page)
            fname = os.path.join(app.config['JSON_FOLDER'],
                                 f"data_{timestamp}_seite{i}.json")
            with open(fname, 'w', encoding='utf-8') as f:
                json.dump(struct, f, ensure_ascii=False, indent=4)

    # 4. Session aufräumen
    for key in ['all_data','page_paths','current_index','session_folder',
                'is_onesite','deleted_pages','reinject_general_data']:
        session.pop(key, None)

    # 5. Redirect-Werte zurückgeben
    return saved_count, deleted_count

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/extract', methods=['POST'])
def extract_data():
    # 1. Alle Dateien aus dem Form-Input auslesen
    files = request.files.getlist('files')  # entspricht <input name="files" multiple>

    print("[DEBUG] extract_data → received files:", [f.filename for f in files])

    if not files or all(f.filename == '' for f in files):
        return "Keine Datei hochgeladen", 400

    # 2. Flags aus dem Formular (gelten für alle Dateien)
    page_range    = request.form.get('page_range', 'all')
    custom_pages  = request.form.get('custom_pages', '').strip()  # "1-3,5"
    selected_sheets = request.form.getlist('sheets')
    is_scanned    = request.form.get('is_scanned', 'false').lower() == 'true'
    is_onesite    = request.form.get('is_onesite', 'false').lower() == 'true'
    session['is_onesite'] = is_onesite

    # 3. Gemeinsamen Session-Ordner und Gesamt-Liste anlegen
    session_folder = tempfile.mkdtemp()
    all_page_paths = []

    # 4. Jede Datei verarbeiten
    for f in files:
        if f.filename == '' or not allowed_file(f.filename):
            continue

        filename = secure_filename(f.filename)
        temp_path = os.path.join(session_folder, filename)
        f.save(temp_path)

        base = os.path.splitext(filename)[0]

        # 4a) Optional OCR
        pdf_path = temp_path
        if is_scanned:
            ocr_path = temp_path.rsplit('.', 1)[0] + '_searchable.pdf'
            scan_to_searchable_pdf(temp_path, ocr_path, dpi=300, lang='deu')
            pdf_path = ocr_path

        # 4b) Excel → PDF
        if filename.lower().endswith(('.xls', '.xlsx')):
            excel_pdf = temp_path.rsplit('.', 1)[0] + '.pdf'
            excel_to_pdf(temp_path, excel_pdf, selected_sheets=selected_sheets)
            pdf_path = excel_pdf

        # 4c) PDF in einzelne Seiten zerlegen
        if page_range == 'custom' and custom_pages:
            paths = split_pdf_into_pages(
                pdf_path,
                session_folder,
                page_range=custom_pages,
                prefix=base
            )
        else:
            paths = split_pdf_into_pages(
                pdf_path,
                session_folder,
                prefix=base
            )
        print(f"[DEBUG] split_pdf_into_pages → returned {len(paths)} paths:", paths)
        print(f"[DEBUG] Für {filename} generierte Seiten: {len(paths)} → {paths}")
        print(f"[DEBUG] extract_data → page_paths: {len(all_page_paths)} items:", all_page_paths)

        # 4d) Seiten-Pfadliste erweitern
        all_page_paths.extend(paths)

    print(f"Seitenbereich: {page_range}")
    print(f"Benutzerdefinierte Seiten: {custom_pages}")
    print(f"Ausgewählte Excel-Sheets: {selected_sheets}")
    print(f"Eine Baustelle? {is_onesite}")
    print(request.form)
    print(f"Gescanntes Dokument? {is_scanned}")

    # 5. In der Session speichern und zum nächsten Schritt weiterleiten
    session['page_paths']    = all_page_paths
    session['current_index'] = 0
    session['session_folder'] = session_folder

    print(f"[DEBUG] extract_data → final session['page_paths'] ({len(all_page_paths)}):", all_page_paths)
    print(f"[DEBUG] session['page_paths'] hat jetzt {len(all_page_paths)} Einträge")

    return redirect(url_for('process_page'))



@app.route('/process_page', methods=['GET'])
def process_page():
    page_paths = session.get('page_paths', [])
    index = session.get('current_index', 0)
    is_onesite = request.args.get('is_onesite', session.get('is_onesite', False))

    print(f"[DEBUG] process_page → current_index={index}, total_pages={len(page_paths)}")

    if index >= len(page_paths):
        deleted_pages = session.get('deleted_pages', [])
        saved_count = len(page_paths) - len(deleted_pages)
        deleted_count = len(deleted_pages)
        return redirect(url_for('danke', saved_count=saved_count, deleted_count=deleted_count))

    current_pdf = page_paths[index]
    data = run_app(current_pdf)
    is_last_page = (index == len(page_paths) - 1)

    if 'all_data' not in session:
        session['all_data'] = []

    # Spezialfall: Wenn die erste Seite gelöscht wurde, stelle auf der nächsten Seite die allgemeinen Daten bereit.
    if session.get('reinject_general_data') and index == 1:
        is_onesite = True  # sicherstellen
        data['is_first_page'] = True
        session.pop('reinject_general_data', None)  # Nur einmalig verwenden

    return render_template('edit.html', labels=labels, current_index=index + 1, total=len(page_paths),
                           is_last_page=is_last_page, is_onesite=is_onesite, **data)


@app.route('/next_page', methods=['POST'])
def next_page():
    index = session.get('current_index', 0)
    page_paths = session.get('page_paths', [])

    form_data = request.form.to_dict(flat=False)
    print(f"[DEBUG] Speichere Seite {index + 1}: {form_data}")

    # Speichern der Formulardaten
    all_data = session.get('all_data') or []

    # Liste auffüllen (z.B. bei gelöschten Seiten)
    while len(all_data) <= index:
        all_data.append(None)

    all_data[index] = copy.deepcopy(form_data)
    session['all_data'] = all_data
    print(f"[DEBUG] all_data now has {len(all_data)} entries:", all_data)

    # Optional: JSON-Backup
    temp_folder = os.path.join(JSON_FOLDER, 'temp')
    os.makedirs(temp_folder, exist_ok=True)
    with open(os.path.join(temp_folder, f'raw_page_{index + 1}.json'), 'w', encoding='utf-8') as f:
        json.dump(form_data, f, ensure_ascii=False, indent=4)

    # Redirect je nach Position
    if index + 1 >= len(page_paths):
        deleted_pages = session.get('deleted_pages', [])
        saved_count = len(page_paths) - len(deleted_pages)
        deleted_count = len(deleted_pages)
        print(
            f"[DEBUG] Letzte Seite erreicht → redirect zu /danke mit saved_count: {saved_count} and deleted_count: {deleted_count}")
        return redirect(url_for('danke', saved_count=saved_count, deleted_count=deleted_count))

    session['current_index'] = index + 1
    return redirect(url_for('process_page'))


@app.route('/update-graph', methods=['POST'])
def update_graph():
    measurement_data = request.get_json()
    graph_data_url = create_measurement_graph(measurement_data)
    return jsonify({'graph': graph_data_url})

@app.route('/delete_page', methods=['POST'])
def delete_page():
    index = session.get('current_index', 0)
    page_paths = session.get('page_paths', [])
    deleted_pages = session.get('deleted_pages', [])

    if index not in deleted_pages:
        deleted_pages.append(index)
        # Wenn die erste Seite gelöscht wird und es sich um eine Baustelle handelt,
        # setze den Flag zur Re-Injektion der allgemeinen Daten
        if session.get('is_onesite', False) and index == 0:
            session['reinject_general_data'] = True
    session['deleted_pages'] = deleted_pages

    # Stelle sicher, dass all_data an dieser Stelle mindestens bis zum aktuellen Index existiert
    all_data = session.get('all_data', [])
    while len(all_data) <= index:
        all_data.append(None)
    session['all_data'] = all_data

    session['current_index'] = index + 1
    if session['current_index'] >= len(page_paths):
        saved, deleted_cnt = finalize_and_cleanup()
        return redirect(url_for('danke', saved_count=saved,
                                deleted_count=deleted_cnt))

    return redirect(url_for('process_page'))


@app.route('/save', methods=['POST'])
def save_data():
    # Aktuelle Formulardaten der letzten Seite speichern, falls vorhanden.
    index = session.get('current_index', 0)
    form_data = request.form.to_dict(flat=False)
    if form_data:
        all_data = session.get('all_data', [])
        # Falls es noch nicht genügend Elemente in der Liste gibt, erweitern wir sie mit None.
        while len(all_data) <= index:
            all_data.append(None)
        # Überschreibe die aktuellen Seiten-Daten in der Session.
        all_data[index] = copy.deepcopy(form_data)
        session['all_data'] = all_data

    # Debug-Ausgaben zur Überprüfung
    print("[DEBUG] Save aufgerufen")
    print("[DEBUG] session['all_data']:", session.get('all_data'))
    print("[DEBUG] session['deleted_pages']:", session.get('deleted_pages'))

    # Falls das Formular angibt, dass es sich um einen One-Site-Fall handelt:
    if 'one_site' in form_data and form_data['one_site'][0] == 'on':
        session['is_onesite'] = True

    is_onesite = session.get('is_onesite', False)
    all_data = session.get('all_data', [])
    deleted_pages = set(session.get('deleted_pages', []))

    # Filtere nur die Seiten, die nicht gelöscht wurden und tatsächlich Daten enthalten
    filtered_data = [
        data for i, data in enumerate(all_data)
        if i not in deleted_pages and data is not None
    ]

    page_paths = session.get('page_paths', [])
    saved_count = len(page_paths) - len(deleted_pages)
    deleted_count = len(deleted_pages)
    print(f"[DEBUG] Gespeicherte Seiten: {saved_count}, Gelöschte Seiten: {deleted_count}")

    if not filtered_data:
        return redirect(url_for('danke'))

    # Erstelle das JSON-Verzeichnis, falls es nicht existiert.
    if not os.path.exists(app.config['JSON_FOLDER']):
        os.makedirs(app.config['JSON_FOLDER'])

    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')

    if is_onesite:
        full_data = {}
        for i, single_page_data in enumerate(filtered_data):
            structured = structured_data(
                single_page_data,
                is_onesite=True,
                is_first_page=(i == 0)
            )
            if i == 0:
                full_data.update(structured)
            else:
                full_data[f"measurement_{i + 1}"] = structured["measurement"]

        filename = os.path.join(app.config['JSON_FOLDER'], f'data_{timestamp}.json')
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(full_data, f, ensure_ascii=False, indent=4)
    else:
        for i, single_page_data in enumerate(filtered_data, start=1):
            structured = structured_data(single_page_data)
            filename = os.path.join(app.config['JSON_FOLDER'], f'data_{timestamp}_seite{i}.json')
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(structured, f, ensure_ascii=False, indent=4)

    # Aufräumen der Session-Daten, damit keine alten Informationen hängen bleiben
    session.pop('all_data', None)
    session.pop('page_paths', None)
    session.pop('current_index', None)
    session.pop('session_folder', None)
    session.pop('is_onesite', None)
    session.pop('deleted_pages', None)

    return redirect(url_for('danke', saved_count=saved_count, deleted_count=deleted_count))

@app.route('/danke')
def danke():
    saved_count = request.args.get('saved_count', 0, type=int)
    deleted_count = request.args.get('deleted_count', 0, type=int)

    # Session-Schlüssel löschen (falls noch Reste da sind)
    for key in ['all_data', 'page_paths', 'current_index', 'session_folder',
                'is_onesite', 'deleted_pages', 'reinject_general_data']:
        session.pop(key, None)

    return render_template('save.html',
                           saved_count=saved_count,
                           deleted_count=deleted_count)


if __name__ == '__main__':
    if not os.path.exists(JSON_FOLDER):
        os.makedirs(JSON_FOLDER)
    app.run(debug=True)
