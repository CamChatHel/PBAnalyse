import win32com.client
import pythoncom
import os

def excel_to_pdf(excel_file, pdf_file, selected_sheets=None):
    pythoncom.CoInitialize()
    excel = win32com.client.Dispatch("Excel.Application")
    excel.Visible = False
    excel.DisplayAlerts = False

    excel_file = os.path.abspath(excel_file)
    wb = excel.Workbooks.Open(excel_file)

    try:
        if selected_sheets:
            sheets_to_export = []
            for name in selected_sheets:
                try:
                    _ = wb.Sheets(name)
                    sheets_to_export.append(name)
                except Exception:
                    print(f"WARNUNG: Blatt '{name}' wurde nicht gefunden und wird übersprungen.")

            if sheets_to_export:
                wb.Sheets(sheets_to_export).Select()
                wb.ActiveSheet.ExportAsFixedFormat(0, os.path.abspath(pdf_file))
                return

        # Fallback: erstes Blatt
        ws = wb.Worksheets(1)
        ws.ExportAsFixedFormat(0, os.path.abspath(pdf_file))

    finally:
        wb.Close(False)
        excel.Quit()

if __name__ == "__main__":
    excel_to_pdf("datei.xlsx", "ausgabe.pdf", selected_sheets=["Tabelle1", "Tabelle2"])
