import os
import traceback
import pdfplumber

debug = 0

def detect_scanned(fname):
    scanned = False
    pdf_doc = pdfplumber.open(fname)
    pages = pdf_doc.pages
    if debug: logger.info("\n number of pages : {}".format(len(pages)))
    total_text = ""
    for ind, page in enumerate(pages):
        try:
            page_extract = page.extract_text()
            if page_extract != None: return False
            else: scanned = True
            if debug: logger.info("\n page number :{}{}".format(ind,scanned))

        except Exception as e:
            if str(e) == 'None':
                print("Raised Exception PDF could not be extracted : PDF Not readable using PDFplumber")
            else:
                print("\n Error in extract_html == ",traceback.format_exc())
            scanned = True

    return scanned


if __name__ == "__main__":
    ### Test
    fname = "dataset/digital.pdf"
    # fname = "dataset/scanned.pdf"
    scanned = detect_scanned(fname)
    print("\n scanned : ", scanned)