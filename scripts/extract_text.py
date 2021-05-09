import os
import re
import cv2
import fitz
from pdf2image import convert_from_path
import pytesseract

import config as cf 


def digital_text(file_path):
    """ extracts text from digital pdf """
    doc = fitz.open(file_path)
    page_count = doc.pageCount
    print("\n number of pages : ",page_count)
    total_text = ""
    try:
        for page_num in range(page_count):
            p = doc.loadPage(page_num)
            page_text = p.getText()
            total_text += page_text
        print("\n number of pages extracted : ", (page_count))
    except Exception as e:
        print("\n Error in digital_text : ", traceback.format_exc(()))
    return total_text


def extract_scanned(file_path):
    """ converts pdf file into images, 1 image per page """
    total_text = ""
    output_folder = os.path.join(cf.data_path, "images")
    try:
        images = convert_from_path(file_path, dpi=300, output_folder=output_folder, first_page=1, last_page=None, fmt='jpg',
                                  thread_count=1, userpw=None)
        image_name = images[0].filename
        for page_num in range(len(images)):
            image = cv2.imread(images[page_num].filename)
            text = pytesseract.image_to_string(image, lang="eng", config='--psm 6')
            total_text += text
        print("\n number of pages extracted : ", len(images))
    except Exception as e:
        print("\n Error in convert2image : ", traceback.format_exc(()))
    return total_text


def extract_text(file_path):
    total_text=""
    total_text = digital_text(file_path)
    if total_text: print("\n digital pdf !!! ") 
    else:
        print("\n scanned pdf !!! ")
        total_text = extract_scanned(file_path)
    return total_text
# file_path = os.path.join(cf.dataset_path, "scanned.pdf")
# image_folder = cf.dataset_path
# extract_scanned(file_path, images_folder)