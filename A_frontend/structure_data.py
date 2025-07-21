def structured_data(form_data, is_onesite=False, is_first_page=False):
    if is_onesite:
        result = {}

        if is_first_page:
            # Allgemeine Daten nur auf Seite 1
            result["allgemeines"] = {
                "baustelle_data": {k: form_data[k][0] for k in sorted(form_data) if k.startswith("baustelle_data")},
                "land_data": {k: form_data[k][0] for k in sorted(form_data) if k.startswith("land_data")},
            }

        result["measurement"] = {
            "pruef_gen_data": {k: form_data[k][0] for k in sorted(form_data) if k.startswith("pruef_gen_data")},
            "sonstiges_data": {k: form_data[k][0] for k in sorted(form_data) if k.startswith("sonstiges_data")},
            "pruef_bt_data": [
                {k: form_data[k][0] for k in sorted(form_data) if k.startswith("pruef_bt_data")},
                {k: form_data[k][0] for k in sorted(form_data) if k.startswith("pruef_bt_id")},
                {k: form_data[k][0] for k in sorted(form_data) if k.startswith("pruef_bt_beschreibung")},
                {k: form_data[k][0] for k in sorted(form_data) if k.startswith("pruef_bt_material")},
                {k: form_data[k][0] for k in sorted(form_data) if k.startswith("pruef_bt_masse")},
                {k: form_data[k][0] for k in sorted(form_data) if k.startswith("pruef_bt_dicke")}
            ],
            "pruef_raum_data": {k: form_data[k][0] for k in sorted(form_data) if k.startswith("pruef_raum_data")},
            "messart_data": {k: form_data[k][0] for k in sorted(form_data) if k.startswith("messart_data")},
            "spectrum_data": {k: form_data[k][0] for k in sorted(form_data) if k.startswith("spectrum_data")},
            "measurement_data": {k: form_data[k][0] for k in sorted(form_data) if k.startswith("measurement_data")},
        }

        return result

    # Struktur für Einzelseiten (NICHT onesite)
    return {
        "baustelle_data": {k: form_data[k][0] for k in sorted(form_data) if k.startswith("baustelle_data")},
        "land_data": {k: form_data[k][0] for k in sorted(form_data) if k.startswith("land_data")},
        "sonstiges_data": {k: form_data[k][0] for k in sorted(form_data) if k.startswith("sonstiges_data")},
        "pruef_gen_data": {k: form_data[k][0] for k in sorted(form_data) if k.startswith("pruef_gen_data")},
        "pruef_bt_data": [
            {k: form_data[k][0] for k in sorted(form_data) if k.startswith("pruef_bt_data")},
            {k: form_data[k][0] for k in sorted(form_data) if k.startswith("pruef_bt_id")},
            {k: form_data[k][0] for k in sorted(form_data) if k.startswith("pruef_bt_beschreibung")},
            {k: form_data[k][0] for k in sorted(form_data) if k.startswith("pruef_bt_material")},
            {k: form_data[k][0] for k in sorted(form_data) if k.startswith("pruef_bt_masse")},
            {k: form_data[k][0] for k in sorted(form_data) if k.startswith("pruef_bt_dicke")}
        ],
        "pruef_raum_data": {k: form_data[k][0] for k in sorted(form_data) if k.startswith("pruef_raum_data")},
        "messart_data": {k: form_data[k][0] for k in sorted(form_data) if k.startswith("messart_data")},
        "spectrum_data": {k: form_data[k][0] for k in sorted(form_data) if k.startswith("spectrum_data")},
        "measurement_data": {k: form_data[k][0] for k in sorted(form_data) if k.startswith("measurement_data")},
    }
