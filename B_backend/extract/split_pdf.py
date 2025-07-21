import os
from PyPDF2 import PdfReader, PdfWriter
import re

def split_pdf_into_pages(pdf_path, output_folder, page_range=None, prefix=""):
    reader = PdfReader(pdf_path)
    num_pages = len(reader.pages)

    if page_range:
        # "1-3,5,7-8" → [1,2,3,5,7,8]
        pages = []
        for part in re.split(r',\s*', page_range):
            if '-' in part:
                start, end = map(int, part.split('-'))
                pages.extend(range(start, end + 1))
            else:
                pages.append(int(part))
        pages = [p - 1 for p in pages if 0 < p <= num_pages]
    else:
        pages = list(range(num_pages))

    output_paths = []
    for i in pages:
        writer = PdfWriter()
        writer.add_page(reader.pages[i])
        output_path = os.path.join(output_folder, f'{prefix}_page_{i + 1}.pdf')
        with open(output_path, 'wb') as f_out:
            writer.write(f_out)
        output_paths.append(output_path)

    return output_paths
