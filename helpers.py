import os

from PyPDF2 import PdfFileReader
from math import floor
import logging
from datetime import datetime
import nltk
from google.cloud import vision
import io
from pdf2image import convert_from_path
from os.path import exists
from nltk.corpus import stopwords
nltk.download('stopwords')
nlp_url='https://language.googleapis.com/v1/documents'


class Helpers:
    @staticmethod
    def extract_pdf(pdf_path):
        with open(pdf_path, 'rb') as f:
            pdf=PdfFileReader(f)
            information=pdf.getDocumentInfo()
            if information is not None:
                author = information.author
                creator = information.creator
                producer = information.producer
                title = information.title
                subject = information.subject
            else:
                author = 'author'
                creator = 'creator'
                producer = 'producer'
                title = 'title'
                subject = 'subject'

            number_of_pages=pdf.getNumPages()
            extracted_text=''
            for x in range(number_of_pages):
                page_obj=pdf.getPage(x)
                extracted_text+=page_obj.extractText()
            if page_obj is None or extracted_text == '':
                extracted_text = letsgo(pdf_path)
            print(extracted_text)
        print(pdf_path)
        return {'text': extracted_text, 'author': author,
                'creator': creator, 'producer': producer, 'title': title,
                'subject': subject,'pages': number_of_pages}

    # https://cloud.google.com/natural-language/pricing
    @staticmethod
    def cost_calculator(text, request_type):
        switch={'entity': 1.0,
                'sentiment': 1.0,
                'syntax': 0.5,
                'entity_sentiment': 2.0,
                'content_classification': 2.0}
        chars=len(text)
        if chars < 1000:
            units, cost=1, switch.get(request_type)
        else:
            units, cost=floor(len(text) / 1000), (floor(len(text) / 1000) * switch.get(request_type))
    #boobs
        logging.log(1, f'\nchars: {chars}'
                       f'\nunits: {units}'
                       f'\ncosts: {cost}'
                       f'\ndate: {datetime.now()}')

        return chars, units, cost

def convert(path):
    cwd = os.getcwd()
    pages = convert_from_path(path, 500, poppler_path=cwd+'\\poppler-0.68.0\\bin')
    count = 1
    for page in pages:
        page.save(f'out{count}.png', 'PNG')
        count+=1
    return len(pages)

def detect_text(path):
    client = vision.ImageAnnotatorClient()

    with io.open(path, 'rb') as image_file:
        content = image_file.read()

    image = vision.Image(content=content)

    response = client.text_detection(image=image)
    texts = response.text_annotations

    full = ""
    for text in texts:
        full += text.description
    return full

def letsgo(path):
    pages = convert(path)
    full = ""
    current = os.getcwd()
    file_exists = exists(current + '\\out1.png')
    if file_exists:
        for x in range(pages):
            if x>0:
                full += detect_text(current + f'\\out{x}.png')
                os.remove(current + f'\\out{x}.png')
    else:
        print("error finding file")
    return full
print('hi')