## Weiterentwicklung eines Werkzeugs <br>zur Extraktion und Verarbeitung bauakustischer Daten<br>  aus Prüfberichten der D-A-CH-Region
 **_im Rahmen einer Studienarbeit von Anna-Magdalena Danner_** 
_Datum: 24.07.2025_

**Python-Projekt: Tool_Pruefbericht_Daten_V2.0**   

> Dieses Werkzeug ermöglicht eine direkte Datenübertragung aus Prüfprotokollen von Bauakustikmessungen der D-A-CH-Region. Relevante Daten werden dabei automatisch extrahiert, standardisiert und gespeichert, ohne dass weitere manuelle Eingaben erforderlich sind. Zusätzlich wird ein KI-Modul integriert, welches komplexe Dateninhalte interpretiert und entsprechenden Datensätzen zuordnet.   
  
## Installation  
 **1.** Stellen Sie sicher, dass Python in der Version 3.12.8 ([Python](https://www.python.org/downloads/release/python-3128/)) und pip ([pip](https://pip.pypa.io/en/stable/installation/)) auf Ihrem Gerät installiert sind.
 
**2.** Installieren Sie Poppler  ([Poppler für Windows]((https://github.com/oschwartz10612/poppler-windows/releases))) und fügen Sie den Pfad des `bin`-Verzeichnisses `C:\Pfad\zu\Poppler\bin`  zu  den Systemumgebungsvariablen (path) hinzu. 

**3.** Installieren Sie Tesseract OCR ([tesseract](https://github.com/tesseract-ocr/tesseract/releases/)) und fügen Sie den Pfad `C:\Pfad\zu\Tesseract-OCR` zu den Systemumgebungsvariablen (path) hinzu. 
Stellen Sie sicher, dass sich im Verzeichnis *tessdata* die Datei für die deutsche Sprache *deu.traineddata* befindet. Falls die Datei fehlt, installieren Sie diese manuell ([deu](https://github.com/tesseract-ocr/tessdata/blob/main/deu.traineddata)) und speichern Sie die Datei im Verzeichnis *tessdata*. 

**4.** Laden Sie das Projekt *'Tool_Pruefbericht_Daten_V2.0'* in einem Verzeichnis Ihrer Wahl.
 
**5.** Öffnen Sie ein Terminal, z.B. PowerShell von Windows und navigieren Sie zu dem Projektverzeichnis:  
```bash  
	cd Pfad\zu\Tool_Pruefbericht_Daten_V2.0
```  
**6.** Erstellen Sie eine virtuelle Umgebung und aktivieren Sie diese:  
```bash  
	python -m venv venv
	venv\Scripts\activate  
``` 
**7.** Installieren Sie die Pakete aus `requirements.txt` und führen Sie das Setup aus:  
```bash  
	pip install -r requirements.txt
	pip install -e .
```  
> **Hinweis**: Je nach Konfiguration des Terminals kann es notwendig sein, anstelle `python` den Befehl `py` zu verwenden.  
>  
## Nutzung  
**1.** Erstellen Sie einen OpenAI-Account. [OpenAI](https://platform.openai.com/signup)  

**2.** Erstellen Sie nach der Registrierung eine Organisation und generieren Sie einen API-Schlüssel:  *Start building > Create organization*.
Folgen Sie den angezeigten Schritten bis *'Generate API Key'*.  

**3.** Kopieren Sie den angezeigten API-Schlüssel und speichern Sie ihn an einem sicheren Ort.  

**4.** Fügen Sie Ihre Zahlungsinformationen hinzu.  

**5.** Erstellen Sie im Hauptverzeichnis des Projekts eine Datei  `key.env` und fügen Ihren persönlichen API-Schlüssel ein:  
```bash
	API_KEY="YOUR_API_KEY" 
```
**6.** Führen Sie im Terminal des Projektverzeichnisses den Befehl aus:  
```bash  
	python A_frontend/web.py
```  
**7.** Es startet ein lokaler Server und ein Link wird in der Konsole angezeigt.  
    Öffnen Sie den Link mit *strg + klick* in einem Webbrowser, um die Anwendung zu nutzen. 
    
**8.** Laden Sie in der Anwendung ein Prüfprotokoll und bestätigen Sie den Upload. Sie werden zur Datenüberprüfung weitergeleitet.   
