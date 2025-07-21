"""
Suchmuster für die Erfassung von Informationen aus Texten
"""

#baustelle_1
messbuero_pattern = r"(Messbuero|Messstelle|Pruefinstitut|Pruefstelle|Messbueros|Pruefinstituts)"
messbueros = r"AKUSTIKBUERODAHMS GmbH|Kurz und Fischer GmbH|MUELLER-BBM|ACCON GmbH|IB Bloedt|PMI GmbH|ig-bauphysik GmbH und Co. KG"
messbuero_map = {
    "MUELLER-BBM": "Müller-BBM",
    "MUeLLER-BBM" : "Müller-BBM",
    "IG BAUPHYSIK GMBH & CO. KG": "ig-bauphysik GmbH & CO. KG"
}

baujahr_pattern = r"(Baujahr|Errichtung|errichtet|Fertigstellung)\s*[:;,.]?\s*(\d{1,2})[./]?\s*(\d{1,2})[./]?\s*(\d{4})"

#Bautypen
massivbau_pattern = ["Stahlbetonbau", "STBbau", "STB-Bau", "Betonbau", "Mauerwerksbau", "Steinbau",
                      "Ziegelhaus", "Kalksandsteinhaus", "schwere Bauweise", "Massivbau", "Massivbauweise",
                      "Massivbaukonstruktion", "Fertigteilbau", "Leichtbetonbau"]
stahlbau_pattern = ["Stahleichtbau", "Stahlbau", "Stahlkonstruktion",
                     "Stahltragwerk", "Leichtstahlbau"]
holzmassivbau_pattern = ["Holzmassivbau", "Massivholzbau", "Brettsperrholzbau", "Brettstapelbau",
                          "Brettschichtholzbau", "Leimholzbau", "Holzmodulbau", "Holzmodul",
                          "Holzbau", "Vollholzbau", "Massivholzhaus", "Blockbau", "Blockhaus", "Holzhaus",
                          "Holzkonstruktion", "Holzblockbau", "Holzblockhaus", "Holzblockbauweise"]
rahmenbau_pattern = ["Holzrahmen", "Tafelbau", "Skelettbau", "Holzskelettbau", "Holzrahmenbau",
                      "Stahlrahmenbau", "Stahlrahmenbauweise"]
fachwerk_pattern = ["Riegelhaus", "Stabwerk", "Fachwerkbau", "Fachwerkhaus"]
holzleichtbau_pattern = ["Leichtholzbau", "Holzstaenderbauweise", "Holzrahmenbauweise", "Holztafelbauweise",
                          "Holzriegelbauweise", "Holzstaenderbau", "Holzrahmenbau", "Holztafelbau",
                          "Holzriegelbau"]

#baustelle_2_land
adress_pattern = r"(Objekt|Adresse|Anschrift|Standort|Ort)"

#pruef_1_gen
date_pattern = r"(Messdatum|Datum der Messung|Datum der Pruefung|Pruefdatum)"
date_format =[
    '%d.%m.%Y', '%d-%m-%Y', '%d/%m/%Y', '%d%m%Y',
    '%d.%m.%y', '%d-%m-%y', '%d/%m/%y', '%d%m%y',
    '%d %B %Y', '%d %b %Y', '%d %B %y', '%d %b %y',
    '%Y.%m.%d', '%Y-%m-%d', '%Y/%m/%d', '%Y%m%d',
    '%y.%m.%d', '%y-%m-%d', '%y/%m/%d', '%y%m%d',
    '%d. %b %Y', '%d. %B %Y'
]
messrichtung_pattern = r"\b(horizontal|horizontale|vertikal|vertikale|diagonal|diagonale|45°)\b"
richtung_pattern = r"Messrichtung|Richtung der Messung|Richtung"
zustand_pattern = r"(Neubau|Altbau|Sanierung|Rohbau)"
anlass_pattern = r"(Bauabnahme|Beschwerde|Nachweis|Gutachten|Anderer)"

#pruef_2_gen
trennbauteil_pattern = r"\b(Trennbauteil\w*|Pruefobjekt\w*|Pruefgegenstand\w*|Aufbau\w*|Pruefanordnung\w*|Bauteilaufbau\w*)\b"
flanke_pattern = (r"\b((F|f)lanken|(F|f)lanke|(F|f)lankierende\s+(B|b)auteile\b[:]*|flankierenden Bauteile|(F|f)lanken+(B|b)auteile\b[:]*|"
                  r"(F|f)lankierende\s+(T|t)rennbauteile\b[:]*|(F|f)lankierend\b[:]*|Anschluesse\b[:]*|Anschluss\b[:]*|flank. Bauteil[e]?\b[:]*)\b"
                  r"|(F|f)lankierende (W|w)aende\b[:]*|(F|f)lankierende (D|d)ecke\n\b[:]*")

trennbauteil_end =(
    r"\b("
    r"Aufbau|Trennbauteil|Pruefobjekt|Pruefgegenstand|Messbuero|Messstelle|Pruefinstitut|Pruefstelle|"
    r"Messbueros|Pruefinstituts|Baujahr|Errichtung|errichtet|Fertigstellung|"
    r"Objekt|Adresse|Anschrift|Standort|Ort|horizontal|horizontale|vertikal|vertikale|diagonal|diagonale|"
    r"Messrichtung|Neubau|Altbau|Sanierung|Rohbau|Bauabnahme|Beschwerde|Nachweis|Gutachten|"
    r"Anderer|Senderaum|Empfangsraum|Trennflaeche|Flaeche|Pruefflaeche|"
    r"Besonderheiten|Bemerkungen|Sonstiges|Anmerkungen|Bemerkung|Besonderheit|Sonstige"
    r")\b:?")

#pruef_3_raum
wohnen_pattern = [
    r"(Wohnen\w*|Wohnzimmer\w*|Kochen\w*|Kueche\w*|Essen\w*|Bad\w*|Badezimmer\w*|Appartement)\s*([\d\w._/-]+)?"
]

schlafen_pattern = [
    r"(Kind\w*|Eltern\w*|Schlafen\w*|Schlafzimmer\w*"
    r"|Kinderzimmer\w*)\s*([\d\w._/-]+)?"
]

schlafen_NWG_pattern = [
    r"(Hotelzimmer\w*|Hotel\w*|Suite\w*|Uebernachtungsraum\w*)\s*([\d\w._/-]+)?"
]

krankenhaus_pattern = [
    r"(Krankenzimmer\w*|Krankenhauszimmer\w*|Krankenhaus\w*|Krankenstation\w*)\s*([\d\w._/-]+)?"
]

buero_pattern = [
    r"(Buero\w*|Konferenz\w*|Besprechung\w*|Seminar\w*)\s*([\d\w._/-]+)?"
]

unterricht_pattern = [
    r"(Klassenzimmer\w*|Unterrichtsraum\w*|Schulzimmer\w*|Schulungsraum\w*)\s*([\d\w._/-]+)?"
]

sonstiger_aufenthalt_pattern = [
    r"(Foyer\w*|Eingang\w*|Party\w*|Pause\w*|Aufenthalt\w*|Tee\w*|Kantine\w*|Loggia\w*|Terrasse\w*)\s*([\d\w._/-]+)?"
]

technik_pattern = [
    r"(Technik\w*|Archiv\w*|Kopier\w*)\s*([\d\w._/-]+)?"
]

nebenraum_pattern = [
    r"(Keller\w*|Party\w*|Treppe\w*|Aufzug\w*|Flur\w*|Dusch\w*)\s*([\d\w._/-]+)?"
]

aussenbereich_pattern = [
    r"(Aussenbereich\w*|Aussen|Hof|Balkon|Aussenraum|Terrasse|Dachterrasse)\s*([\d\w._/-]+)?"
]

raumart_patterns = [
            (wohnen_pattern, "Wohnen in WG"),
            (schlafen_pattern, "Schlafen in WG"),
            (schlafen_NWG_pattern, "Uebernachtungsraum in NWG"),
            (krankenhaus_pattern, "Bettenraum in Krankenanstalt"),
            (buero_pattern, "Buero"),
            (unterricht_pattern, "Unterrichtsraum"),
            (sonstiger_aufenthalt_pattern, "Sonstiger Aufenthaltsraum"),
            (technik_pattern, "Technikraum"),
            (nebenraum_pattern, "Nebenraum"),
            (aussenbereich_pattern, "Aussenbereich")
]

vol_pattern = r'(\d+[.,]?\d*|[-/]\s*|)\s*(m3|m³|m\^3)'
senderaum_pattern = r"([S|s]enderaum|[S|s]ende|SR)"
empfangraum_pattern = r"([E|e]mpfangsraum|[E|e]mpfang|ER|[E|e]mpfangraum|[E|e]mpfangsraum[es|s]?)"

flaeche_context_pattern = r"(Trennflaeche|Trennbauteil|Pruefobjekt|Pruefgegenstand|Flaeche|A|F)"
trennflaeche_pattern = r"(\d+([.,]\d+)?\s*(m²|m\^2|m2|sq))"

#messwerte_2_C
equation_pattern = r"\(\s*C\s*;\s*Ctr\s*\)\s*=\s*(\d+)\s*\(\s*([-\d]+)\s*;\s*([-\d]+)\s*\)\s*dB"

#sonstiges
else_pattern = r"(Besonderheiten|Besonderheiten:|Bemerkungen|Sonstiges|Anmerkungen|Anmerkungen:|Anmerkung:|Bemerkung|Besonderheit|Sonstige)"

#Endmuster
end_patterns = (messbuero_pattern + r"|" + baujahr_pattern + r"|" + adress_pattern + r"|" + date_pattern + r"|"
                + messrichtung_pattern + r"|" + "Senderaum" + r"|" +
                "Empfangsraum" + r"|" + "Aufbau" + r"|" +
                equation_pattern + r"|" + else_pattern+ r"|" + zustand_pattern + r"|" + anlass_pattern + r"|" + richtung_pattern)