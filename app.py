import os
import requests
from config import api_key
import json
from flask import Flask, render_template, request
from flask_restful import Resource, Api, reqparse
from PyPDF2 import PdfFileReader

app=Flask(__name__)
api=Api(app)
app.config['UPLOAD_FOLDER']=r'Z:\.GCP\natural_language_poc\pdfs'


class AnalyzeEntities(Resource):
    def post(self) -> list:
        parser=reqparse.RequestParser()
        parser.add_argument('text', required=True)  # add args
        args=parser.parse_args()

        body={
            "document": {
                "type": "PLAIN_TEXT",
                "language": "EN",
                "content": args.get('text')
            },
            "encodingType": "UTF8"
        }
        response=requests.post('https://language.googleapis.com/v1beta2/documents:analyzeEntities'
                               f'?key={api_key}',
                               data=json.dumps(body))
        d=json.loads(response.text)
        return [d.get('entities')[i].get('name') for i, x in enumerate(d.get('entities'))]


class PDFAnalyzeEntities(Resource):
    def post(self) -> list:
        if request.method == 'POST':
            f=request.files['file']
            path=os.path.join(app.config['UPLOAD_FOLDER'], f.filename)
            f.save(path)
            text=extract_pdf(path)

            body={
                "document": {
                    "type": "PLAIN_TEXT",
                    "language": "EN",
                    "content": text
                },
                "encodingType": "UTF8"
            }
            response=requests.post('https://language.googleapis.com/v1beta2/documents:analyzeEntities'
                                   f'?key={api_key}',
                                   data=json.dumps(body))
            d=json.loads(response.text)
            print(d)
            return [d.get('entities')[i].get('name') for i, x in enumerate(d.get('entities'))]


class AnalyzeEntitySentiment(Resource):
    def post(self) -> list:
        parser=reqparse.RequestParser()
        parser.add_argument('text', required=True)  # add args
        args=parser.parse_args()

        body={
            "document": {
                "type": "PLAIN_TEXT",
                "language": "EN",
                "content": args.get('text')
            },
            "encodingType": "UTF8"
        }
        response=requests.post('https://language.googleapis.com/v1beta2/documents:analyzeEntitySentiment'
                               f'?key={api_key}',
                               data=json.dumps(body))
        d=json.loads(response.text)
        print(d)
        return [d.get('entities')[i].get('name') for i, x in enumerate(d.get('entities'))]


class PDFAnalyzeEntitySentiment(Resource):
    def post(self) -> list:
        f=request.files['file']
        path=os.path.join(app.config['UPLOAD_FOLDER'], f.filename)
        f.save(path)
        text=extract_pdf(path)

        body={
            "document": {
                "type": "PLAIN_TEXT",
                "language": "EN",
                "content": text
            },
            "encodingType": "UTF8"
        }
        response=requests.post('https://language.googleapis.com/v1beta2/documents:analyzeEntitySentiment'
                               f'?key={api_key}',
                               data=json.dumps(body))
        d=json.loads(response.text)
        print(d)

        return [(d.get('entities')[i].get('name'),
                 [(mention.get('text').get('content'),
                   mention.get('type'),
                   mention.get('sentiment').get('magnitude'),
                   mention.get('sentiment').get('score')) for mention in d.get('entities')[i].get('mentions')])
                for i, x in enumerate(d.get('entities'))
                if True in [True if mention.get('type') != 'COMMON' and
                            mention.get('sentiment').get('magnitude') > 0 or
                            mention.get('sentiment').get('score') > 0
                            else False
                            for mention in d.get('entities')[i].get('mentions')]]


def extract_pdf(pdf_path):
    with open(pdf_path, 'rb') as f:
        pdf=PdfFileReader(f)
        information=pdf.getDocumentInfo()
        number_of_pages=pdf.getNumPages()
        extracted_text=''
        for x in range(number_of_pages):
            page_obj=pdf.getPage(x)
            extracted_text+=page_obj.extractText()

    pdf_details=f"""
    Information about {pdf_path}:\nAuthor: {information.author}
    Creator: {information.creator}\nProducer: {information.producer}
    Subject: {information.subject}\nTitle: {information.title}\nNumber of pages: {number_of_pages}
    """
    return extracted_text


@app.route('/upload_pdf')
def upload_pdf():
    return render_template('upload.html')


api.add_resource(AnalyzeEntities, '/analyze_entities')
api.add_resource(AnalyzeEntitySentiment, '/analyze_entity_sentiment')
api.add_resource(PDFAnalyzeEntities, '/pdf/analyze_entities')
api.add_resource(PDFAnalyzeEntitySentiment, '/pdf/analyze_entity_sentiment')

if __name__ == '__main__':
    # extract_pdf(r'Z:\.GCP\natural_language_poc\pdfs\Adam Siwiec UM form.pdf')
    app.run()
