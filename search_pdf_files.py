import PyPDF2
import re
from os import listdir
from os.path import isfile, join

file_list = get_files_from_path("file_path")
print(search_pdfs_for_text("search_text", file_list))

def get_files_from_path(input_file_path):
    return [f for f in listdir('.\\') if isfile(join('.\\', f))]

def search_pdfs_for_text(input_text, pdf_file_list):
    matched_pdf_file_list = []
    for pdf_file in pdf_file_list:
            pdf_object = PyPDF2.PdfFileReader(pdf_file)
            num_pages = pdf_object.getNumPages()
            for i in range(0, num_pages):
                    page_object = pdf_object.getPage(i)
                    page_text = page_object.extractText()
                    search_result = re.search(input_text, page_text)
                    if search_result != None:
                            matched_pdf_file_list.append(pdf_file)
    return list(set(matched_pdf_file_list))