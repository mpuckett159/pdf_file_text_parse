import PyPDF2
import re
from os import listdir
from os.path import isfile, join
import sys
import requests
import shutil
import time
import pprint

### example
### python .\search_pdf_files.py 'OPA_Case_Folder' 'dog' 'no' 'True'

def download_pdf_files(url_list,destination_dir):
    for url in url_list:
        local_filename = destination_dir + '\\' + url.split('/')[-1]
        with requests.get(url, stream=True) as r:
            with open(local_filename, 'wb') as f:
                shutil.copyfileobj(r.raw, f)
        time.sleep(5)


def get_files_from_path(input_file_path):
    return [f for f in listdir(input_file_path) if isfile(join(input_file_path, f))]

def search_pdfs_for_text(input_text, pdf_file_list, source_dir):
    matched_pdf_file_list = []
    for pdf_file in pdf_file_list:
            pdf_object = PyPDF2.PdfFileReader(source_dir + '\\' + pdf_file)
            num_pages = pdf_object.getNumPages()
            for i in range(0, num_pages):
                    page_object = pdf_object.getPage(i)
                    page_text = page_object.extractText()
                    search_result = re.search(input_text, page_text)
                    if search_result != None:
                            matched_pdf_file_list.append(pdf_file)
    return list(set(matched_pdf_file_list))

if sys.argv[3] != "no":
    print("Downloading files to " + sys.argv[1])
    download_pdf_files(sys.argv[3],sys.argv[1])
print("Getting files from " + sys.argv[1])
file_list = get_files_from_path(sys.argv[1])
relevant_pdfs = search_pdfs_for_text(sys.argv[2], file_list, sys.argv[1])
pprint.pprint(relevant_pdfs)
if sys.argv[4] == "True":
    print("Writing case numbers out to text file")
    with open('relevant_pdfs.txt','a') as txtfile:
        for pdf in relevant_pdfs:
            txtfile.write(pdf + '\n')