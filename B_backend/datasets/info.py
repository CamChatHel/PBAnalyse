"""
Ergänzende Informationen
"""

get_bautypen = ["Massivbau",
         "Holzmassivbau",
         "Stahlbau",
         "Rahmenbau",
         "Fachwerk",
         "Holzleichtbau",
         "Andere"
         ]

get_bundeslaender_de = [
        "Baden-Wuerttemberg", "Bayern", "Berlin", "Brandenburg", "Bremen", "Hamburg", "Hessen",
        "Mecklenburg-Vorpommern", "Niedersachsen", "Nordrhein-Westfalen", "Rheinland-Pfalz",
        "Saarland", "Sachsen", "Sachsen-Anhalt", "Schleswig-Holstein", "Thueringen"
    ]

get_bundeslaender_oe = [
        "Burgenland", "Kaernten", "Niederoesterreich", "Oberoesterreich", "Salzburg", "Steiermark",
        "Tirol", "Vorarlberg", "Wien"
    ]

get_kantone_ch = [
    "Aargau", "Appenzell Ausserrhoden", "Appenzell Innerrhoden", "Basel-Landschaft", "Basel-Stadt",
    "Bern", "Freiburg", "Genf", "Glarus", "Graubuenden", "Jura", "Luzern", "Neuenburg", "Nidwalden",
    "Obwalden", "Schaffhausen", "Schwyz", "Solothurn", "St. Gallen", "Tessin", "Thurgau", "Uri", "Waadt",
    "Wallis", "Zug", "Zuerich"
]

get_land = ["Deutschland", "Oesterreich", "Schweiz"]

get_messrichtung = ["horizontal", "vertikal", "diagonal"]

get_messarten = [
    {"Messart": "Schalldaemmung Fassadenbauteil", "M_ID": 3,
     "Begriffe": ["Schalldaemmung Fassadenbauteil", "Fassadenbauteil", "Fassadenschalldaemmung", "16283-3", "DIN EN ISO 16283-3",
                  "Bauteil-Verfahren", "Bauteil-Straßenverkehr-Verfahren", "Bauteil-Lautsprecher-Verfahren"],
     "Parameter": {"R'45°": "Bau-Schalldaemm-Mass Fassadenbauteil",
                   "R'tr, s": "Bau-Schalldaemm-Mass Strassenverkehr",
                   "R'rt, s": "Bau-Schalldaemm-Mass Fassadenbauteil, Schienenverkehr",
                   "R'at, s": "Bau-Schalldaemm-Mass Fassadenbauteil, Luftverkehr"}},
    {"Messart": "Luftschalldaemmung", "M_ID": 1,
     "Begriffe": ["Luftschalldaemmung", "Luftschallmessung", "16283-1", "DIN EN ISO 16283-1",
                  "ISO 140-4"],
     "Parameter": {"R'": "Bau-Schalldaemm-Mass", "Dn": "Norm-Schallpegeldifferenz",
                   "DnT": "Standard-Schallpegeldifferenz", "D": "Schallpegeldifferenz"}},
    {"Messart": "Trittschalldaemmung", "M_ID": 2,
     "Begriffe": ["Trittschalldaemmung", "Trittschall", "Trittschallmessung", "16283-2", "DIN EN ISO 16283-2",
                  "ISO 140-5"],
     "Parameter": {"L'n": "Norm-Trittschallpegel", "L'nT": "Standard-Trittschallpegel"}},
    {"Messart": "Schalldaemmung Fassade ganz", "M_ID": 4,
     "Begriffe": ["Schalldaemmung Fassade ganz", "16283-3", "DIN EN ISO 16283-3", "ISO 140-7", "Gesamt-Verfahren",
                "Gesamt-Straßenverkehr-Verfahren", "Gesamt-Lautsprecher-Verfahren"],
     "Parameter": {"Dls, 2m, nT": "Standard-Schallpegeldifferenz Fassade ganz",
        "Dls, 2m, n": "Norm-Schallpegeldifferenz Fassade ganz",
        "Dtr, 2m, nT": "Standard-Schallpegeldifferenz Fassade ganz, Strassenverkehr",
        "Dtr, 2m, n": "Norm-Schallpegeldifferenz Fassade ganz, Strassenverkehr",
        "Drt, 2m, nT": "Standard-Schallpegeldifferenz Fassade ganz, Schienenverkehr",
        "Drt, 2m, n": "Norm-Schallpegeldifferenz Fassade ganz, Schienenverkehr",
        "Dat, 2m, nT": "Standard-Schallpegeldifferenz Fassade ganz, Luftverkehr",
        "Dat, 2m, n": "Norm-Schallpegeldifferenz Fassade ganz, Luftverkehr"}},
]

def get_mess_id():
    return {
        "Schalldaemmung Fassadenbauteil": 3,
        "Luftschalldaemmung": 1,
        "Trittschalldaemmung": 2,
        "Schalldaemmung Fassade ganz": 4
    }

def get_description():
    return {
        "R'45°": "Bau-Schalldaemm-Mass Fassadenbauteil",
        "R'tr, s": "Bau-Schalldaemm-Mass Fassadenbauteil, Strassenverkehr",
        "R'rt, s": "Bau-Schalldaemm-Mass Fassadenbauteil, Schienenverkehr",
        "R'at, s": "Bau-Schalldaemm-Mass Fassadenbauteil, Luftverkehr",
        "D": "Schallpegeldifferenz",
        "Dn": "Norm-Schallpegeldifferenz",
        "DnT": "Standard-Schallpegeldifferenz",
        "R'": "Bau-Schalldaemm-Mass",
        "L'n": "Norm-Trittschallpegel",
        "L'nT": "Standard-Trittschallpegel",
        "Dls, 2m, nT": "Standard-Schallpegeldifferenz Fassade ganz",
        "Dls, 2m, n": "Norm-Schallpegeldifferenz Fassade ganz",
        "Dtr, 2m, nT": "Standard-Schallpegeldifferenz Fassade ganz, Strassenverkehr",
        "Dtr, 2m, n": "Norm-Schallpegeldifferenz Fassade ganz, Strassenverkehr",
        "Drt, 2m, nT": "Standard-Schallpegeldifferenz Fassade ganz, Schienenverkehr",
        "Drt, 2m, n": "Norm-Schallpegeldifferenz Fassade ganz, Schienenverkehr",
        "Dat, 2m, nT": "Standard-Schallpegeldifferenz Fassade ganz, Luftverkehr",
        "Dat, 2m, n": "Norm-Schallpegeldifferenz Fassade ganz, Luftverkehr",
        "R'i": "Bau-Schalldaemm-Mass, allgemein",
        "-": "-"
    }


get_parameter_synonyms = {
    "D nT": "DnT",
    "DnT,w": "DnT",
    "D nT,w": "DnT",

    "D n": "Dn",
    "Dn,w": "Dn",
    "D n,w": "Dn",

    "R' 45°": "R'45°",
    "R'45°, w": "R'45°",
    "R` 45°": "R'45°",
    "R' 45": "R'45°",
    "R` 45": "R'45°",
    "R'45,w": "R'45°",
    "R'45°,w": "R'45°",
    "R' 45,w": "R'45°",
    "R' 45°,w": "R'45°",
    "R´45,w": "R'45°",
    "R´ 45,w": "R'45°",

    "R' tr,s": "R'tr,s",
    "R` tr,s": "R'tr,s",
    "R'tr,w": "R'tr,s",
    "R´tr,w": "R'tr,s",
    "R' tr,w": "R'tr,s",
    "R' tr,s,w": "R'tr,s",
    "R´ tr,s,w": "R'tr,s",

    "R`": "R'",
    "R`w": "R'",
    "R',w": "R'",

    "L' nT": "L'nT",
    "L'nT,w": "L'nT",
    "L` nT": "L'nT",
    "L´nT,w": "L'nT",

    "L' n": "L'n",
    "L'n,w": "L'n",
    "L` n": "L'n",
    "L´n,w": "L'n",
}

def get_ps_id():
    return {
        "Schallpegeldifferenz": 1,
        "Norm-Schallpegeldifferenz": 2,
        "Standard-Schallpegeldifferenz": 3,
        "Bau-Schalldaemm-Mass": 4,
        "Norm-Trittschallpegel": 5,
        "Standard-Trittschallpegel": 6,
        "Bau-Schalldaemm-Mass Fassadenbauteil": 7,
        "Bau-Schalldaemm-Mass Fassadenbauteil, Strassenverkehr": 8,
        "Bau-Schalldaemm-Mass Fassadenbauteil, Schienenverkehr": 9,
        "Bau-Schalldaemm-Mass Fassadenbauteil, Luftverkehr": 10,
        "Standard-Schallpegeldifferenz Fassade ganz": 11,
        "Norm-Schallpegeldifferenz Fassade ganz": 12,
        "Standard-Schallpegeldifferenz Fassade ganz, Strassenverkehr": 13,
        "Norm-Schallpegeldifferenz Fassade ganz, Strassenverkehr": 14,
        "Standard-Schallpegeldifferenz Fassade ganz, Schienenverkehr": 15,
        "Norm-Schallpegeldifferenz Fassade ganz, Schienenverkehr": 16,
        "Standard-Schallpegeldifferenz Fassade ganz, Luftverkehr": 17,
        "Norm-Schallpegeldifferenz Fassade ganz, Luftverkehr": 18,
        "Bau-Schalldaemm-Mass, allgemein": 19,
        "-":"-"
    }

def get_parameter():
    return {
        "R'45°": {"description": "Bau-Schalldämm-Mass Fassadenbauteil", "ps_id": 7},
        "R'tr, s": {"description": "Bau-Schalldämm-Mass Fassadenbauteil, Straßenverkehr", "ps_id": 8},
        "R'rt, s": {"description": "Bau-Schalldämm-Mass Fassadenbauteil, Schienenverkehr", "ps_id": 9},
        "R'at, s": {"description": "Bau-Schalldämm-Mass Fassadenbauteil, Luftverkehr", "ps_id": 10},
        "D": {"description": "Schallpegeldifferenz", "ps_id": 1},
        "Dn": {"description": "Norm-Schallpegeldifferenz", "ps_id": 2},
        "DnT": {"description": "Standard-Schallpegeldifferenz", "ps_id": 3},
        "R'": {"description": "Bau-Schalldämm-Mass", "ps_id": 4},
        "L'n": {"description": "Norm-Trittschallpegel", "ps_id": 5},
        "L'nT": {"description": "Standard-Trittschallpegel", "ps_id": 6},
        "Dls, 2m, nT": {"description": "Standard-Schallpegeldifferenz Fassade ganz", "ps_id": 11},
        "Dls, 2m, n": {"description": "Norm-Schallpegeldifferenz Fassade ganz", "ps_id": 12},
        "Dtr, 2m, nT": {"description": "Standard-Schallpegeldifferenz Fassade ganz, Straßenverkehr", "ps_id": 13},
        "Dtr, 2m, n": {"description": "Norm-Schallpegeldifferenz Fassade ganz, Straßenverkehr", "ps_id": 14},
        "Drt, 2m, nT": {"description": "Standard-Schallpegeldifferenz Fassade ganz, Schienenverkehr", "ps_id": 15},
        "Drt, 2m, n": {"description": "Norm-Schallpegeldifferenz Fassade ganz, Schienenverkehr", "ps_id": 16},
        "Dat, 2m, nT": {"description": "Standard-Schallpegeldifferenz Fassade ganz, Luftverkehr", "ps_id": 17},
        "Dat, 2m, n": {"description": "Norm-Schallpegeldifferenz Fassade ganz, Luftverkehr", "ps_id": 18},
        "R'i": {"description": "Bau-Schalldämm-Mass, allgemein", "ps_id": 19},
        "-" : {"description": "-", "ps_id": "-"}
    }

get_zustand = ["Neubau", "Altbau", "Sanierung", "Rohbau"]

get_anlass = ["Bauabnahme", "Beschwerde", "Nachweis", "Gutachten", "Anderer"]

get_raumarten = ['Wohnen in WG', 'Schlafen in WG', 'Uebernachtungsraum in NWG', 'Bettenraum in Krankenanstalt',
                 'Buero', 'Unterrichtsraum', 'Sonstiger Aufenthaltsraum', 'Technikraum', 'Nebenraum', 'Aussenbereich']

# Angabe in Kleinbuchstaben, damit auch Wortteile gefunden werden
get_bauteiltypA =["massivwand", "massiv", "beton", "stahlbeton", "kalksandstein", "massivholz", "brettsperrholz", "glas", "metall", "kunststoff", "ziegel", "mauerwerk", "verputzt", "außenputz", "unterputz", "estrich", "naturstein", "fliesen","clt","brettschichtholz"]
get_bauteiltypB = ["trockenbau", "gipskarton", "holzständerwerk", "metallständerwerk", "faserzement", "leichtbauwand", "leichtbau", "leichtbautrennwand", "leichtbauplatte"]
