import pymupdf

def convert_pdf_to_text(filepath, keyword='holdings'):
    pdf_document = pymupdf.open(filepath)
    text = ''
    
    for page in pdf_document:
        page_text = page.get_text()
        # Only append converted text to ouput if keyword is on page
        if keyword.lower() in page_text.lower():
            text += page_text

    pdf_document.close()
    return text