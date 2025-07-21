//Funktionale Komponenten im HTML

//ALLGEMEINE FUNKTIONEN - Loader
window.addEventListener('load', function() {
            document.getElementById('loader').style.display = 'none';
            document.getElementById('overlay').style.display = 'none';
        });

//ALLGEMEINE FUNKTIONEN - Textfelder
function enableEditing(button) {
    const textarea = button.closest('.row').querySelector('textarea'); // Finde das Textarea-Element innerhalb der aktuellen Zeile
    if (textarea) {
        textarea.removeAttribute('readonly'); // Entferne das readonly-Attribut, um die Bearbeitung zu ermöglichen
        console.log(`Readonly entfernt: ${textarea.readOnly}`); // Überprüfe in der Konsole, ob readonly entfernt wurde
        button.style.display = 'none'; // Verberge den Bearbeiten-Button
        textarea.classList.add('highlight'); // Highlight das Textarea-Feld
        if (textarea.value === "-") {
            textarea.value = "";
        }
    } else {
        console.error('Textarea nicht gefunden');
    }
}

//ALLGEMEINE FUNKTIONEN - Dropdown
function enableEditingWithDropdown(button, key) {
    const textarea = document.getElementById(key);
    const dropdown = document.getElementById(key + '_dropdown');

    if (textarea && dropdown) {
        textarea.style.display = 'none';
        dropdown.style.display = 'inline-block';
        dropdown.classList.add('highlight'); // Highlight Dropdown
        dropdown.focus();
        button.style.display = 'none'; // Verberge den Bearbeiten-Button

        // Setze den Dropdown-Wert auf den aktuellen Textarea-Wert
        dropdown.value = textarea.value;

        // Aktualisiere das Textarea-Feld mit dem aktuellen Dropdown-Wert bei Dropdown-Änderung
        dropdown.addEventListener('change', function () {
            textarea.value = dropdown.options[dropdown.selectedIndex].text; // Nur den Text speichern
        });
        // Sofortige Speicherung des aktuell angezeigten Werts im Textarea-Feld
        textarea.value = dropdown.options[dropdown.selectedIndex].text; // Setze den Text sofort
    } else {
        console.error('Textarea oder Dropdown nicht gefunden für:', key);
    }

    // Sofortige Speicherung des aktuell angezeigten Werts im Textarea-Feld
    const newValue = dropdownField.value;
    textareaField.value = newValue;
}

//ALLGEMEINE FUNKTIONEN - Gefärbte Felder, wenn Wert leer
function validateFields() {
    // Alle textarea-Felder auswählen
    const fields = document.querySelectorAll('textarea');

    fields.forEach(field => {
        const value = field.value.trim(); // Wert des Felds (ohne Leerzeichen)

        if (value === "-" || value === ""|| value === "0") {
            field.classList.add('error');
        } else {
            field.classList.remove('error');
        }
        // Fehlermeldung ausblenden, wenn Wert korrekt eingegeben wird
        const errorMessage = document.getElementById(`${field.id}-error-message`);
        if (errorMessage) {
            if (value.includes("Bericht") && value.includes("Berechnung")) {
                errorMessage.style.display = 'block';
                field.classList.add('error');
            } else {
                errorMessage.style.display = 'none';
                field.classList.remove('error');
            }
        }
    });
}

//ALLGEMEINE FUNKTIONEN - Gefärbte Felder, wenn Wert leer, beim Laden der Seite
window.onload = function() {
    validateFields(); // Felder beim Laden überprüfen
    // Felder auch bei Änderungen überprüfen
    const textareas = document.querySelectorAll('textarea');
    textareas.forEach(textarea => {
         textarea.addEventListener('input', validateFields); // Event-Listener für Änderungen
    });
};

//DATEN SPEICHERN
document.addEventListener('DOMContentLoaded', () => {
    const saveButton = document.getElementById('saveButton');
    const nextButton = document.getElementById('nextButton');
    const deleteConfirmButton = document.getElementById('deleteConfirmButton');
    const deleteNextButton = document.getElementById('deleteNextButton');
    const confirmButton = document.getElementById('modal-confirm-button');

    if (saveButton) {
        saveButton.addEventListener('click', () => {
            const errorMessage = getErrorMessage();
            if (errorMessage) {
                showModal(errorMessage, false);
            } else {
                showModal("Sind Sie sicher, dass Sie die Daten speichern möchten?", true, () => {
                    if (window.showLoader) {
                        window.showLoader();
                    }
                    saveData();
                });
            }
        });
    }


    if (nextButton) {
        nextButton.addEventListener('click', () => {
            const errorMessage = getErrorMessage();
            if (errorMessage) {
                showModal(errorMessage, false);
            } else {
                showModal("Diese Daten können danach nicht mehr geändert werden. Möchten Sie fortfahren?", true, () => {
                    // Hier fragt deine Logik: Zuerst den Loader anzeigen ...
                    if (window.showLoader) {
                        window.showLoader();
                    } else {
                        console.log("showLoader ist nicht verfügbar");
                    }
                    // Dann das Formular abschicken:
                    document.querySelector('form').submit();
                });
            }
        });
    }

    if (deleteConfirmButton) {
        deleteConfirmButton.addEventListener('click', () => {
            showModal("Möchten Sie diesen Datensatz wirklich löschen?", true, () => {
                submitDeleteForm();
            });
        });
    }

    if (deleteNextButton) {
        deleteNextButton.addEventListener('click', () => {
            showModal("Möchten Sie diesen Datensatz wirklich löschen und mit dem nächsten Protokoll fortfahren?", true, () => {
                if (window.showLoader) {
                    window.showLoader();
                }
                submitDeleteForm();
            });
        });
    }
});

function getErrorMessage() {
    const errorFields = document.querySelectorAll('.error-number');
    const errorMessages = document.querySelectorAll('.message[style*="display: block"]');

    const invalidTextareas = [
        document.getElementById('Messart'),
        document.getElementById('Parameter'),
        document.querySelector('textarea[name="spectrum_data[EINZAHLWERT]"]'),
        ...document.querySelectorAll('textarea[name^="measurement_data["]')
    ];

    const hasInvalidTextareas = Array.from(invalidTextareas).some(textarea => {
        return textarea && (textarea.value === "-" || textarea.value === "");
    });

    if (errorFields.length > 0 || errorMessages.length > 0) {
        return "Bitte korrigieren Sie die Fehler (rot gefärbte Felder), bevor Sie die Daten speichern.";
    }

    if (hasInvalidTextareas) {
        return "Die Felder für Messart, Parameter, Einzahlwert und frequenzabhängige Werte dürfen nicht leer oder unvollständig sein.";
    }

    return null;
}

function saveData() {
    const formData = new FormData();
    document.querySelectorAll('textarea, input').forEach(input => {
        if (input.name) {
            formData.append(input.name, input.value);
        }
    });

    fetch('/save', {
        method: 'POST',
        body: formData
    })
    .then(response => {
        if (response.redirected) {
            window.location.href = response.url;
        } else {
            return response.text();
        }
    })
    .then(data => {
        showModal('Daten wurden erfolgreich gespeichert!', false);
    })
    .catch(error => {
        showModal('Fehler beim Speichern der Daten.', false);
    });
}

function submitDeleteForm() {
    const form = document.createElement('form');
    form.method = 'POST';
    form.action = '/delete_page';

    const hiddenInput = document.createElement('input');
    hiddenInput.type = 'hidden';
    hiddenInput.name = 'delete_index';
    hiddenInput.value = '{{ current_index }}';

    form.appendChild(hiddenInput);
    document.body.appendChild(form);
    form.submit();
}

function showModal(message, isConfirmation, onConfirm = null) {
    const modal = document.getElementById('custom-modal');
    const modalMessage = document.getElementById('modal-message');
    const confirmationButtons = document.getElementById('confirmation-buttons');
    const okButton = document.getElementById('ok-button');

    modalMessage.innerText = message;
    modal.style.display = 'block';

    if (isConfirmation) {
        confirmationButtons.style.display = 'block';
        okButton.style.display = 'none';

        const confirmBtn = document.getElementById('modal-confirm-button');
        const newBtn = confirmBtn.cloneNode(true);
        confirmBtn.parentNode.replaceChild(newBtn, confirmBtn);
        newBtn.addEventListener('click', () => {
            hideModal();
            if (onConfirm) onConfirm();
        });
    } else {
        confirmationButtons.style.display = 'none';
        okButton.style.display = 'block';
    }
}

function hideModal() {
    const modal = document.getElementById('custom-modal');
    modal.style.display = 'none';
}

//Messbüro Dropdown, Eigene Eingabe
function enableMessbueroDropdown(index) {
    // Verstecke das Textfeld
    document.getElementById('MESSBUERO_display_' + index).style.display = 'none';

    // Zeige und aktiviere das Dropdown
    const dropdown = document.getElementById('MESSBUERO_dropdown_' + index);
    dropdown.style.display = 'inline-block';
    dropdown.disabled = false;
    dropdown.classList.add('highlight');

    // Zeige den Button für eigene Eingabe und verstecke den "Bearbeiten"-Button
    document.getElementById('MESSBUERO_custom_input_button_' + index).style.display = 'inline-block';
    document.getElementById('MESSBUERO_edit_button_' + index).style.display = 'none';
}

function enableMessbueroCustomInput(index) {
    // Verstecke das Dropdown und deaktiviere es
    const dropdown = document.getElementById('MESSBUERO_dropdown_' + index);
    dropdown.style.display = 'none';
    dropdown.disabled = true;

    // Zeige das Textfeld, mache es editierbar und setze den Fokus
    const display = document.getElementById('MESSBUERO_display_' + index);
    display.style.display = 'inline-block';
    display.readOnly = false;
    display.disabled = false;
    display.classList.add('highlight');

    // Schalte die Buttons um
    document.getElementById('MESSBUERO_custom_input_button_' + index).style.display = 'none';
    document.getElementById('MESSBUERO_edit_button_' + index).style.display = 'inline-block';
}

function handleMessbueroChange(index) {
    const dropdown = document.getElementById('MESSBUERO_dropdown_' + index);
    const selectedValue = dropdown.value;

    // Aktualisiere das Anzeigefeld
    document.getElementById('MESSBUERO_display_' + index).value = selectedValue;
    // Aktualisiere den Hidden Input, der übermittelt wird
    document.getElementById('MESSBUERO_' + index).value = selectedValue;
}

//BAUJAHR
function validateBaujahr(input) {
    const baujahrError = document.getElementById('baujahr-error');
    const baujahrValue = input.value;
    const baujahrPattern = /^-$|^\d{4}$/;

    // Überprüfen, ob das Baujahr genau 4 Ziffern enthält
    if (baujahrPattern.test(baujahrValue)) {
        baujahrError.style.display = 'none';  // Fehlernachricht ausblenden
        input.style.borderColor = '';  // Standardrahmenfarbe
        input.classList.remove('error-number');
        input.classList.add ('highlight');
    } else {
        baujahrError.style.display = 'block';  // Fehlernachricht anzeigen
        input.style.borderColor = 'red';  // Rahmenfarbe ändern
        input.classList.add('error-number');
        input.classList.remove('highlight');
    }
}


//LAND UND BUNDESLAND/KANTON
function enableEditingForLandAndRegion(button) {
    const landTextarea = document.getElementById("land");
    const landDropdown = document.getElementById("land_dropdown");

    const bundeslandTextarea = document.getElementById("bundeslaender");
    const bundeslandDropdown = document.getElementById("bundeslaender_dropdown");

    landTextarea.style.display = "none";
    landDropdown.style.display = "inline-block";

    bundeslandTextarea.style.display = "none";
    bundeslandDropdown.style.display = "inline-block";

    // Button ausblenden
    button.style.display = "none";
    landDropdown.classList.add ('highlight');
    bundeslandDropdown.classList.add ('highlight');

    // Synchronisiere Land-Textarea, wenn Dropdown geändert wird
    landDropdown.addEventListener("input", () => {
        landTextarea.value = landDropdown.value;
        updateFieldClass(landTextarea);
        updateBundeslandDropdown();  // Bundesland-Dropdown basierend auf Land aktualisieren
    });

    // Synchronisiere Bundesland-Textarea, wenn Dropdown geändert wird
    bundeslandDropdown.addEventListener("input", () => {
        bundeslandTextarea.value = bundeslandDropdown.value;
        updateFieldClass(bundeslandTextarea);
    });

    // Initialisiere das Bundesland-Dropdown basierend auf dem ausgewählten Land
    updateBundeslandDropdown();

    const defaultLand = landTextarea.value || "";
    if (defaultLand) {
        landDropdown.value = defaultLand;
    } else {
        landDropdown.value = "";
    }

    updateFieldClass(landTextarea);
    updateFieldClass(bundeslandTextarea);
}

//BUNDESLAND - Aktualisierung des Dropdowns basierend auf dem ausgewählten Land
function updateBundeslandDropdown() {
    const landDropdown = document.getElementById("land_dropdown");
    const bundeslandDropdown = document.getElementById("bundeslaender_dropdown");
    const bundeslandTextarea = document.getElementById("bundeslaender");

    const selectedLand = landDropdown.value;
    const currentBundesland = bundeslandTextarea.value;

    // Leeren des Bundesland-Dropdowns
    bundeslandDropdown.innerHTML = '';

    // Verfügbare Regionen abrufen
    const availableRegions = regions[selectedLand] || [];
    if (availableRegions.length === 0) {
        const noOption = document.createElement("option");
        noOption.value = "";
        noOption.textContent = "Keine Optionen verfügbar";
        bundeslandDropdown.appendChild(noOption);
        return;
    }

    availableRegions.forEach(region => {
        const option = document.createElement("option");
        option.value = region;
        option.textContent = region;

        if (region === currentBundesland) {
            option.selected = true;
        }
        bundeslandDropdown.appendChild(option);
    });

    // Standardwert setzen
    bundeslandDropdown.value = currentBundesland ? currentBundesland : "";

    updateFieldClass(bundeslandTextarea);
}

//LAND - Aktualisierung der CSS-Klassen
function updateFieldClass(field) {
    const value = field.value.trim();
}

// LAND - Beim Laden des Dokuments initialisieren
document.addEventListener('DOMContentLoaded', function () {
    updateBundeslandDropdown();

    const landTextarea = document.getElementById("land");
    const bundeslandTextarea = document.getElementById("bundeslaender");

    updateFieldClass(landTextarea);
    updateFieldClass(bundeslandTextarea);
});

//MESSDATUM
function enableEditingForDate(button, key) {
    const textareaField = document.getElementById(key);
    const dateField = document.getElementById(key + '_date');

    //Datepicker
    textareaField.style.display = 'none';
    dateField.style.display = 'inline-block';

    button.style.display = 'none';

    //Aktuelle Datum des Textarea-Feldes im Datepicker-Feld
    const dateValue = textareaField.value.split('.').reverse().join('-'); // Umwandlung von dd.mm.yyyy nach yyyy-mm-dd
    dateField.value = dateValue;

    dateField.removeAttribute('readonly');
    dateField.focus();
    dateField.classList.add('highlight');
    dateField.classList.add('date-border');


    // Aktualisieren des Textarea-Felds
    dateField.addEventListener('input', () => {
        const newDateValue = dateField.value.split('-').reverse().join('.'); // Umwandlung von yyyy-mm-dd nach dd.mm.yyyy
        textareaField.value = newDateValue;
    });
}

//VOLUMEN, MASSE
function validateVolume(input) {
    const volumeError = document.getElementById(input.id + '-message');
    const volumeValue = input.value;
    const volumePattern = /^-$|^-?$|^[0-9]+$/;

    // Überprüfen, ob das Volumen/die Masse als ganze Zahl angegeben ist
    if (volumePattern.test(volumeValue)) {
        volumeError.style.display = 'none';
        input.style.borderColor = '';
        input.classList.remove('error-number');
        input.classList.add ('highlight');
    } else {
        volumeError.style.display = 'block';
        input.style.borderColor = 'red';
        input.classList.add ("error-number");
        input.classList.remove('highlight');
    }
}

//TRENNFLÄCHE
function validateArea(input) {
    const areaError = document.getElementById(input.id + '-message');
    const areaValue = input.value;
    const areaPattern = /^-$|^[0-9]{1,4}\.[0-9]{2}$/;

    // Überprüfen, ob die Fläche mit 2 Dezimalstellen angegeben ist
    if (areaPattern.test(areaValue)) {
        areaError.style.display = 'none';
        input.style.borderColor = '';
        input.classList.remove('error-number');
        input.classList.add ('highlight');
    } else {
        areaError.style.display = 'block';
        input.style.borderColor = 'red';
        input.classList.add ("error-number");
        input.classList.remove('highlight');
    }
}

//DICKE
function validateDimension(input) {
    const dimError = document.getElementById(input.id + '-message');
    const dimValue = input.value;
    const dimPattern = /^-$|^[0-9]{1,4}(\.[0-9])?$/;

    // Überprüfen, ob die Dicke mit max 1 Dezimalstellen angegeben ist
    if (dimPattern.test(dimValue)) {
        dimError.style.display = 'none';
        input.style.borderColor = '';
        input.classList.remove('error-number');
        input.classList.add ('highlight');
    } else {
        dimError.style.display = 'block';
        input.style.borderColor = 'red';
        input.classList.add ("error-number");
        input.classList.remove('highlight');
    }
}

//INFOBOX
function toggleInfo(id) {
  const box = document.getElementById(id);
  box.style.display = (box.style.display === 'block') ? 'none' : 'block';
}


//EINZAHLWERT
function validateSingleNumber(input) {
    const SingleNumberError = document.getElementById(input.id + '-message');
    const SingleNumberValue = input.value;
    const SingleNumberPattern = /^[0-9]{1,3}$/;

    // Überprüfen, ob der Einzahlwert mit 0-1 Dezimalstellen angegeben ist
    if (SingleNumberPattern.test(SingleNumberValue)) {
        SingleNumberError.style.display = 'none';
        input.style.borderColor = '';
        input.classList.remove('error-number');
        input.classList.add ('highlight');
    } else {
        SingleNumberError.style.display = 'block';
        input.style.borderColor = 'red';
        input.classList.add ("error-number");
        input.classList.remove('highlight');
    }
}

//MESSWERTE
function toggleTableEditing(button) {
    const table = button.closest('table');
//alle Textfelder innerhalb der Tabelle
    const textareas = table.querySelectorAll('.measurement-table textarea');

    textareas.forEach(textarea => {
        if (textarea.hasAttribute('readonly')) {
            textarea.removeAttribute('readonly');
            textarea.classList.add('highlight');
        } else {
            validateMeasurement(textarea);
            textarea.setAttribute('readonly', true);
            textarea.classList.remove('highlight');
            }
    });
    button.style.display = 'none';
}

function validateMeasurement(input) {
    const measurePattern = /^\/$|^[0-9]+\.[0-9]$/;
    const errorSpan = document.getElementById(input.id + '-message');
    const value = input.value;
        if (measurePattern.test(value)) {
            errorSpan.style.display = 'none';
            input.style.borderColor = '';
            input.classList.remove('error-number');
            input.classList.add('highlight');
        } else {
            errorSpan.style.display = 'block';
            input.style.borderColor = 'red';
            input.classList.add('error-number');
            input.classList.remove('highlight');
        }
}

//MESSWERTE - Event-Listener zur Überprüfung von Änderungen während der Bearbeitung
document.querySelectorAll('.measurement-table textarea').forEach(textarea => {
    textarea.addEventListener('input', function() {
        validateMeasurement(textarea);
    });
});

//SPEKTRUMANPASSUNGSWERT
function toggleSpectrumTableEditing(button) {
    // Hole die spezifische Tabelle, deren Button angeklickt wurde
    const table = button.closest('table');

    // Alle Textfelder innerhalb dieser speziellen Tabelle
    const textareas = table.querySelectorAll('textarea');

    textareas.forEach(textarea => {
        if (textarea.hasAttribute('readonly')) {
            textarea.removeAttribute('readonly');
            textarea.classList.add('highlight');
        } else {
            // Muster
            validateSpectrum(textarea);
            textarea.setAttribute('readonly', true);
            textarea.classList.remove('highlight');
        }
    });

    button.style.display = 'none';
}

function validateSpectrum(input) {
    const spectrumPattern = /^-$|^-?[0-9]{1,2}$/;
    const errorSpan = document.getElementById(input.id + '-message');
    const value = input.value;

    if (spectrumPattern.test(value)) {
        errorSpan.style.display = 'none';
        input.style.borderColor = '';
        input.classList.remove('error-number');
        input.classList.add('highlight');
    } else {
        errorSpan.style.display = 'block';
        input.style.borderColor = 'red';
        input.classList.add('error-number');
        input.classList.remove('highlight');
    }
}

// Event-Listener Spektrumanpassungswert
document.querySelectorAll('.spectrum-table textarea').forEach(textarea => {
    textarea.addEventListener('input', function() {
        validateSpectrum(textarea);
    });
});

//Spektrumanpassungswerte abhängig der Messart
function updateSpectrumTable() {
    const messart = document.getElementById('Messart_dropdown').value;
    console.log(`Aktuelle Messart: ${messart}`);  // Debugging: Aktuelle Messart anzeigen

    const rows = document.querySelectorAll('.spectrum-row');

    rows.forEach(row => {
        const key = row.getAttribute('data-key');
        console.log(`Überprüfe Zeile: ${key}`);  // Debugging: Schlüssel anzeigen

        if (messart === 'Trittschalldaemmung') {
            if (key === 'CI' || key === 'CI50B2500') {
                row.style.display = '';
            } else {
                row.style.display = 'none';
            }
        } else {
            if (key === 'CI' || key === 'CI50B2500') {
                row.style.display = 'none';
            } else {
                row.style.display = '';
            }
        }
    });
}


//TRENNBAUTEIL, FLANKEN, MESSART, PARAMETER, IDs
// Aktualisieren der Trennbauteil-ID
function updateTrennbauteilID() {
    const dropdown = document.getElementById('Trennbauteil_dropdown');
    const trennbauteilID = document.getElementById('Trennbauteil_ID');
    if (dropdown && trennbauteilID) {
        const selectedOption = dropdown.value;
        trennbauteilID.value = selectedOption;
        console.log('Trennbauteil-ID aktualisiert:', selectedOption);
    }
}

// Aktualisieren der Flanken-IDs
function updateFlankeID(index) {
    const dropdown = document.getElementById('Flanke' + index + '_dropdown');
    const flankeID = document.getElementById('Flanke' + index + '_ID');
    if (dropdown && flankeID) {
        const selectedOption = dropdown.value;
        flankeID.value = selectedOption;
        console.log(`Flanke${index}-ID aktualisiert:`, selectedOption);
    }
}

// Aktualisieren der Messart-ID
function updateMessartID() {
    const dropdown = document.getElementById('Messart_dropdown');
    const messartID = document.getElementById('Messart_ID');
    if (dropdown && messartID) {
        const selectedOption = dropdown.value;
        const selectedMessartData = messParaId.find(m => m.Messart === selectedOption);
        messartID.value = selectedMessartData ? selectedMessartData.M_ID : '';
        console.log('Messart-ID aktualisiert:', messartID.value);
    }
}

// Aktualisieren der Parameterbeschreibung und PS_ID
function updateParameterOptions() {
    const messartDropdown = document.getElementById('Messart_dropdown');
    const parameterDropdown = document.getElementById('Parameter_dropdown');
    const descriptionTextarea = document.getElementById('Beschreibung');
    const psIdTextarea = document.getElementById('PS_ID');

    if (messartDropdown && parameterDropdown) {
        const selectedMessart = messartDropdown.value;

        parameterDropdown.innerHTML = ''; // Dropdown leeren

        if (selectedMessart && selectedMessart !== '-') {
            const selectedMessartData = messParaId.find(m => m.Messart === selectedMessart);

            if (selectedMessartData && selectedMessartData.Parameter) {
                const placeholderOption = document.createElement('option');
                placeholderOption.value = '';
                placeholderOption.text = '-';
                parameterDropdown.appendChild(placeholderOption);

                Object.keys(selectedMessartData.Parameter).forEach(key => {
                    const option = document.createElement('option');
                    option.value = key;
                    option.text = key || 'Unbekannter Parameter';
                    parameterDropdown.appendChild(option);
                });

                console.log(`Parameter-Optionen aktualisiert für Messart: ${selectedMessart}`);
            } else {
                console.warn('Keine gültigen Parameter für die ausgewählte Messart gefunden.');
            }
        }

        // Beschreibung und PS_ID auf "-" setzen, wenn keine Parameter vorhanden sind
        descriptionTextarea.value = '-';
        psIdTextarea.value = '-';
        console.log('Beschreibung und PS_ID auf "-" gesetzt, da keine Parameter vorhanden sind.');
    } else {
        console.error('Messart-Dropdown oder Parameter-Dropdown fehlt.');
    }
}

function updateParameterDescription() {
    const parameterDropdown = document.getElementById('Parameter_dropdown');
    const descriptionTextarea = document.getElementById('Beschreibung');
    const psIdTextarea = document.getElementById('PS_ID');

    if (parameterDropdown && descriptionTextarea && psIdTextarea) {
        const selectedParameterKey = parameterDropdown.value;

        if (!selectedParameterKey) { // Wenn kein Parameter ausgewählt ist
            descriptionTextarea.value = '-';
            psIdTextarea.value = '-';
            console.warn('Parameterbeschreibung und PS_ID auf "-" gesetzt, da kein gültiger Parameter ausgewählt ist.');
            return;
        }

        const selectedMessart = document.getElementById('Messart_dropdown').value;
        const selectedMessartData = messParaId.find(m => m.Messart === selectedMessart);

        if (selectedMessartData && selectedMessartData.Parameter[selectedParameterKey]) {
            const description = selectedMessartData.Parameter[selectedParameterKey];
            descriptionTextarea.value = description;

            const psId = ps_id[description] || '-';
            psIdTextarea.value = psId;

            console.log('Beschreibung aktualisiert:', description);
            console.log('PS_ID aktualisiert:', psId);
        } else {
            descriptionTextarea.value = '-';
            psIdTextarea.value = '-';
            console.warn('Parameterbeschreibung und PS_ID auf "-" gesetzt, da kein gültiger Parameter vorhanden ist.');
        }
    } else {
        console.error('Fehlende Elemente für die Aktualisierung der Parameterbeschreibung.');
    }
}

// Event-Listener initialisieren
function initializeEventListeners() {
    document.addEventListener('DOMContentLoaded', () => {
        const messartDropdown = document.getElementById('Messart_dropdown');
        const parameterDropdown = document.getElementById('Parameter_dropdown');
        const descriptionTextarea = document.getElementById('Beschreibung');
        const psIdTextarea = document.getElementById('PS_ID');

    // Backend-Initialwerte sichern
        const initialDescription = descriptionTextarea.value.trim();
        const initialPsId = psIdTextarea.value.trim();
        const initialParameter = parameterDropdown.value; // Speichert den initial gewählten Parameter

        if (messartDropdown) {
            messartDropdown.addEventListener('change', () => {
                updateMessartID();
                updateParameterOptions();
                descriptionTextarea.value = '-';
                psIdTextarea.value = '-';
                updateSpectrumTable();
            });

            updateSpectrumTable();
        }

        if (parameterDropdown) {
            parameterDropdown.addEventListener('change', updateParameterDescription);
        }

    // Parameter sofort laden
        updateParameterOptions();

    // Warte kurz auf Backend-Werte, bevor Parameter gesetzt werden
        setTimeout(() => {
        // Falls Backend-Werte existieren, setze sie
            if (initialParameter && initialParameter !== '-') {
                parameterDropdown.value = initialParameter;
                updateParameterDescription(); // Beschreibung und PS_ID aktualisieren
            }

            if (initialDescription && initialDescription !== '-') {
                descriptionTextarea.value = initialDescription;
                console.log('Beschreibung aus Backend übernommen:', initialDescription);
            } else {
                updateParameterDescription();
            }

            if (initialPsId && initialPsId !== '-') {
                psIdTextarea.value = initialPsId;
                console.log('PS_ID aus Backend übernommen:', initialPsId);
            } else {
                updateParameterDescription();
            }
        }, 100); // 100ms Verzögerung für Backend-Daten
    });
}

initializeEventListeners();

// Plot
let debounceTimer = null;

function debouncedUpdateGraph() {
    clearTimeout(debounceTimer);
    debounceTimer = setTimeout(updateGraph, 500);  // Warte 500ms nach letzter Eingabe
}

function updateGraph() {
    const data = {};
    const textareas = document.querySelectorAll('textarea[name^="measurement_data["]');

    textareas.forEach(area => {
        const key = area.name.match(/measurement_data\[(.*?)\]/)[1];
        const value = area.value;
        data[key] = value;
    });

    fetch('/update-graph', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    }).then(response => response.json())
      .then(result => {
          const img = document.querySelector('#measurement-graph');
          img.src = result.graph;
      });
}