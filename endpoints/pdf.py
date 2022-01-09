import os
import requests
from config import api_key, upload_folder
import json
from flask import request, Blueprint
from helpers import Helpers, nlp_url

h=Helpers()
pdf_analyze_entities_bp=Blueprint('pdf_analyze_entities_endpoint', __name__)
pdf_analyze_entity_sentiment_bp=Blueprint('pdf_analyze_entity_sentiment_endpoint', __name__)


@pdf_analyze_entities_bp.route('/pdf/analyze_entities', methods=['POST'])
def pdf_analyze_entities():
    if request.method == 'POST':
        f=request.files['file']
        path=os.path.join(upload_folder, f.filename)
        f.save(path)
        pdf=h.extract_pdf(path)
        body={"document": {
            "type": "PLAIN_TEXT",
            "language": "EN",
            "content": pdf.get('text')
        }, "encodingType": "UTF8"}

        response=requests.post(f'{nlp_url}:analyzeEntities'
                               f'?key={api_key}',
                               data=json.dumps(body))
        d=json.loads(response.text)
        print(d)
        h.cost_calculator(pdf.get('text'), 'entity')
        return json.dumps({'author': pdf.get('author'),
                           'title': pdf.get('title'),
                           'subject': pdf.get('subject'),
                           'pages': pdf.get('pages'),
                           'entities:': [d.get('entities')[i].get('name') for i, x in enumerate(d.get('entities'))]})


@pdf_analyze_entity_sentiment_bp.route('/pdf/analyze_entity_sentiment', methods=['POST'])
def pdf_analyze_entity_sentiment():
    f=request.files['file']
    path=os.path.join(upload_folder, f.filename)
    f.save(path)
    pdf=h.extract_pdf(path)
    body={"document": {
        "type": "PLAIN_TEXT",
        "language": "EN",
        "content": pdf.get('text')
    }, "encodingType": "UTF8"}

    response=requests.post(f'{nlp_url}:analyzeEntitySentiment'
                           f'?key={api_key}',
                           data=json.dumps(body))
    d=json.loads(response.text)
    print(d)
    h.cost_calculator(pdf.get('text'), 'entity_sentiment')
    return json.dumps({'author': pdf.get('author'),
                       'title': pdf.get('title'),
                       'subject': pdf.get('subject'),
                       'pages': pdf.get('pages'),
                       'mentions': [
                           [(dict(zip(['name', 'content', 'beginOffset', 'type', 'salience', 'magnitude', 'score'],
                                      (d.get('entities')[i].get('name'),
                                       mention.get('text').get('content'),
                                       mention.get('text').get('beginOffset'),
                                       mention.get('type'),
                                       mention.get('salience'),
                                       mention.get('sentiment').get('magnitude'),
                                       mention.get('sentiment').get('score'))))) for mention in
                            d.get('entities')[i].get('mentions')]
                           for i, x in enumerate(d.get('entities'))
                           if d.get('entities')[i].get('name') in [d.get('entities')[i].get('name')
                                                                   for mention in d.get('entities')[i].get('mentions')
                                                                   if mention.get('sentiment').get('magnitude') > 0 or
                                                                   mention.get('sentiment').get('score') > 0]]})
