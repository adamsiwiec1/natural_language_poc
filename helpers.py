from PyPDF2 import PdfFileReader
from math import floor
import logging
from datetime import datetime

nlp_url='https://language.googleapis.com/v1/documents'


class Helpers:
    @staticmethod
    def extract_pdf(pdf_path):
        with open(pdf_path, 'rb') as f:
            pdf=PdfFileReader(f)
            information=pdf.getDocumentInfo()

            number_of_pages=pdf.getNumPages()
            extracted_text=''
            for x in range(number_of_pages):
                page_obj=pdf.getPage(x)
                extracted_text+=page_obj.extractText()
        print(pdf_path)
        return {'text': extracted_text, 'author': information.author,
                'creator': information.creator, 'producer': information.producer, 'title': information.title,
                'subject': information.subject,'pages': number_of_pages}

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

print('hi')