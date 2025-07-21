let loadedPdf = null;
let thumbnailsDiv = null;

function parseCustomPages(input, maxPage) {
    const result = new Set();
    const parts = input.split(',');
    parts.forEach(part => {
        const [start, end] = part.split('-').map(p => parseInt(p.trim()));
        if (!isNaN(start)) {
            if (end && !isNaN(end)) {
                for (let i = start; i <= end && i <= maxPage; i++) {
                    result.add(i);
                }
            } else {
                if (start <= maxPage) result.add(start);
            }
        }
    });
    return [...result].sort((a, b) => a - b);
    console.log(selectedPages);
}


async function renderPdfPreview(pdf, pages = null) {
    thumbnailsDiv.innerHTML = '';
    const numPages = pdf.numPages;
    const pagesToRender = pages || Array.from({ length: numPages }, (_, i) => i + 1);

    for (let i of pagesToRender) {
        if (i < 1 || i > numPages) continue;
        const page = await pdf.getPage(i);
        const scale = 1.5;
        const viewport = page.getViewport({ scale });

        const canvas = document.createElement("canvas");
        const context = canvas.getContext("2d");

        const outputScale = window.devicePixelRatio || 1;
        canvas.width = Math.floor(viewport.width * outputScale);
        canvas.height = Math.floor(viewport.height * outputScale);
        canvas.style.width = `${viewport.width * 0.2}px`;
        canvas.style.height = `${viewport.height * 0.2}px`;
        context.setTransform(outputScale, 0, 0, outputScale, 0, 0);

        await page.render({ canvasContext: context, viewport }).promise;

        const dataUrl = canvas.toDataURL("image/png");

        const link = document.createElement("a");
        link.href = dataUrl;
        link.setAttribute("data-fancybox", "pdf-preview");
        link.setAttribute("data-caption", `Seite ${i}`);
        link.appendChild(canvas);

        const wrapper = document.createElement("div");
        wrapper.classList.add("fancybox-thumb-wrapper");

        const pageLabel = document.createElement("div");
        pageLabel.classList.add("pdf-page-label");
        pageLabel.innerText = `Seite ${i}`;

        wrapper.appendChild(link);
        wrapper.appendChild(pageLabel);
        thumbnailsDiv.appendChild(wrapper);
    }
}

document.addEventListener("DOMContentLoaded", function () {
    const fileInput = document.getElementById('fileInput');
    const dropArea = document.getElementById("drop-area");


    ["dragenter", "dragover", "dragleave", "drop"].forEach(event => {
        dropArea.addEventListener(event, e => e.preventDefault());
    });


    ["dragenter", "dragover"].forEach(event => {
        dropArea.addEventListener(event, () => dropArea.classList.add("highlight"));
    });

    ["dragleave", "drop"].forEach(event => {
        dropArea.addEventListener(event, () => dropArea.classList.remove("highlight"));
    });

    dropArea.addEventListener("drop", event => {
        event.preventDefault();
        dropArea.classList.remove("highlight");

        const files = event.dataTransfer.files;
        if (files.length) {
            fileInput.files = files;
            fileInput.dispatchEvent(new Event("change"));
        }
    });


    thumbnailsDiv = document.getElementById('thumbnails');

    let loadedPdfs = [];

    const form = document.getElementById('uploadForm');
    form.addEventListener('submit', function () {
        const checkbox = document.getElementById('is_scanned');
        checkbox.setAttribute('value', checkbox.checked ? 'true' : 'false');
        document.getElementById('loader').style.display = 'block';
        document.getElementById('overlay').style.display = 'block';
    });

    fileInput.addEventListener('change', async function () {
        if (!fileInput.files.length) return;

        thumbnailsDiv.innerHTML = '';
        pageSelection.style.display = 'none';
        previewContainer.style.display = 'none';
        excelSheetSelection.style.display = 'none';

        loadedPdfs = [];

        const files = Array.from(fileInput.files);
        const pdfPromises = files.map(file => {
            const fileType = file.name.split('.').pop().toLowerCase();
            if (fileType === 'pdf') {
                return new Promise((resolve, reject) => {
                    const reader = new FileReader();
                    reader.onload = async function () {
                        const typedarray = new Uint8Array(this.result);
                        const pdf = await pdfjsLib.getDocument(typedarray).promise;
                        resolve(pdf);
                    };
                    reader.onerror = reject;
                    reader.readAsArrayBuffer(file);
                });
            } else if (fileType === 'xls' || fileType === 'xlsx') {
                const reader = new FileReader();
                reader.onload = function (e) {
                    const data = new Uint8Array(e.target.result);
                    const workbook = XLSX.read(data, { type: 'array' });

                    sheetCheckboxes.innerHTML = '';
                    workbook.SheetNames.forEach(name => {
                        const checkbox = `<label><input type="checkbox" name="sheets" value="${name}" checked> ${name}</label><br>`;
                        sheetCheckboxes.innerHTML += checkbox;
                    });
                    excelSheetSelection.style.display = 'block';
                };
                reader.readAsArrayBuffer(file);
                return null;
            } else {
                return null;
            }
        });

    const resolvedPdfs = await Promise.all(pdfPromises.filter(Boolean));
    loadedPdfs = resolvedPdfs.filter(Boolean);

    if (loadedPdfs.length) {
        pageSelection.style.display = 'block';
        previewContainer.style.display = 'block';

    // Checkbox "Gescannte Dokumente" immer anzeigen
        document.getElementById("is_scanned_container").style.display = "block";

    // Prüfen, ob mindestens ein Dokument mehrseitig ist
        const fileCount = fileInput.files.length;
        const hasMultiPagePdf = loadedPdfs.some(pdf => pdf.numPages > 1);

        if (fileCount > 1 || hasMultiPagePdf) {
          document.getElementById("is_onesite_container").style.display = "block";
        } else {
          document.getElementById("is_onesite_container").style.display = "none";
        }


        renderMergedPdfPreview(loadedPdfs);
    }
});


    const customPagesInput = document.getElementById('customPagesInput');

    customPagesInput.removeAttribute("disabled");
    console.log("customPagesInput.enabled (nach Laden):", !customPagesInput.disabled);

document.querySelectorAll('input[name="page_range"]').forEach(radio => {
    radio.addEventListener('change', () => {
        customPagesInput.disabled = radio.value !== 'custom';

        if (radio.value === "custom") {
            customPagesInput.removeAttribute("disabled");
            customPagesInput.focus();
        } else {
            customPagesInput.setAttribute("disabled", "true");

            if (radio.value === "all" && loadedPdfs.length > 0) {
                renderMergedPdfPreview(loadedPdfs, null);
            }
        }
    });
});


customPagesInput.addEventListener('input', () => {
    const selected = document.querySelector('input[name="page_range"]:checked');
    if (selected && selected.value === 'custom' && loadedPdfs.length > 0) {
        const pages = parseCustomPages(customPagesInput.value, getTotalPages(loadedPdfs));

        renderMergedPdfPreview(loadedPdfs, pages);
    }
});


function getTotalPages(pdfList) {
    return pdfList.reduce((sum, pdf) => sum + pdf.numPages, 0);
}

async function renderMergedPdfPreview(pdfList, selectedPages = null) {
    thumbnailsDiv.innerHTML = '';
    let allPages = [];

    // Alle Seiten in richtiger Reihenfolge erfassen
    for (const pdf of pdfList) {
        const numPages = pdf.numPages;
        for (let i = 1; i <= numPages; i++) {
            allPages.push({ pdf, page: i });
        }
    }

    // Optional filtern (bei Custom-Auswahl)
    if (selectedPages) {
        allPages = allPages.filter((_, idx) => selectedPages.includes(idx + 1));
    }

    // Seiten rendern (durchgehend nummeriert)
    for (let globalIndex = 0; globalIndex < allPages.length; globalIndex++) {
        const { pdf, page } = allPages[globalIndex];
        const pdfPage = await pdf.getPage(page);

        const scale = 1.5;
        const viewport = pdfPage.getViewport({ scale });

        const canvas = document.createElement("canvas");
        const context = canvas.getContext("2d");

        const outputScale = window.devicePixelRatio || 1;
        canvas.width = Math.floor(viewport.width * outputScale);
        canvas.height = Math.floor(viewport.height * outputScale);
        canvas.style.width = `${viewport.width * 0.2}px`;
        canvas.style.height = `${viewport.height * 0.2}px`;
        context.setTransform(outputScale, 0, 0, outputScale, 0, 0);

        await pdfPage.render({ canvasContext: context, viewport }).promise;

        const dataUrl = canvas.toDataURL("image/png");

        const link = document.createElement("a");
        link.href = dataUrl;
        link.setAttribute("data-fancybox", "pdf-preview");
        link.setAttribute("data-caption", `${globalIndex + 1}`);
        link.appendChild(canvas);

        const wrapper = document.createElement("div");
        wrapper.classList.add("fancybox-thumb-wrapper");

        const pageLabel = document.createElement("div");
        pageLabel.classList.add("pdf-page-label");
        pageLabel.innerText = `${globalIndex + 1}`;

        wrapper.appendChild(link);
        wrapper.appendChild(pageLabel);
        thumbnailsDiv.appendChild(wrapper);
        }
    }
});