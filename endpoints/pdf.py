import json
import os

import requests
from flask import request, Blueprint, render_template
from json2html import json2html

from config import api_key, upload_folder
from helpers import Helpers, nlp_url

h=Helpers()
pdf_analyze_entities_bp=Blueprint('pdf_analyze_entities', __name__)
pdf_analyze_entity_sentiment_bp=Blueprint('pdf_analyze_entity_sentiment', __name__)
pdf_analyze_sentiment_bp=Blueprint('pdf_analyze_sentiment', __name__)
pdf_analyze_syntax_bp=Blueprint('pdf_analyze_syntax', __name__)
pdf_annotate_text_bp=Blueprint('pdf_annotate_text', __name__)
pdf_classify_text_bp=Blueprint('pdf_classify_text', __name__)


@pdf_analyze_entities_bp.route('/pdf/analyze_entities', methods=['POST'])
def analyze_entities():
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
        print(json.dumps(d))
        h.cost_calculator(pdf.get('text'), 'entity')
        x=json.dumps({'author': pdf.get('author'),
                      'title': pdf.get('title'),
                      'subject': pdf.get('subject'),
                      'pages': pdf.get('pages'),
                      'entities:': [d.get('entities')[i].get('name') for i, x in enumerate(d.get('entities'))]})
        print(x)

        return render_template('/shared/partials/table.html', data=[json2html.convert(json=x,
                                                                                      table_attributes="id=\"info-table\" class=\"table table-bordered table-hover\""),
                                                                    x,
                                                                    "analyze_entities_" + pdf.get(
                                                                        'author') + "_" + pdf.get(
                                                                        'title')])


@pdf_analyze_entity_sentiment_bp.route('/pdf/analyze_entity_sentiment', methods=['POST'])
def analyze_entity_sentiment():
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
    x=json.dumps({'author': pdf.get('author'),
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

    return render_template('/shared/partials/table.html', data=[json2html.convert(json=x,
                                                                                  table_attributes="id=\"info-table\" class=\"table table-bordered table-hover\""),
                                                                x,
                                                                "analyze_entity_sentiment_" + pdf.get(
                                                                    'author') + "_" + pdf.get(
                                                                    'title')])


@pdf_analyze_sentiment_bp.route('/pdf/analyze_sentiment', methods=['POST'])
def analyze_sentiment():
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

        response=requests.post(f'{nlp_url}:analyzeSentiment'
                               f'?key={api_key}',
                               data=json.dumps(body))
        d=json.loads(response.text)
        print('sentiment:' + str(d))
        h.cost_calculator(pdf.get('text'), 'content_classification')
        x=json.dumps(d)
        return render_template('/shared/partials/table.html', data=[json2html.convert(json=x,
                                                                                      table_attributes="id=\"info-table\" class=\"table table-bordered table-hover\""),
                                                                    x,
                                                                    "analyze_sentiment_" + pdf.get(
                                                                        'author') + "_" + pdf.get(
                                                                        'title')])


@pdf_analyze_syntax_bp.route('/pdf/analyze_syntax', methods=['POST'])
def analyze_syntax():
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

        response=requests.post(f'{nlp_url}:analyzeSyntax'
                               f'?key={api_key}',
                               data=json.dumps(body))
        d=json.loads(response.text)
        print('classify:' + str(d))
        h.cost_calculator(pdf.get('text'), 'content_classification')
        x=json.dumps(d)
        csv='1,2,3\n4,5,6\n'
        return render_template('/shared/partials/table.html', data=[json2html.convert(json=x,
                                                                                      table_attributes="id=\"info-table\" class=\"table table-bordered table-hover\""),
                                                                    x,
                                                                    "analyze_syntax_" + pdf.get(
                                                                        'author') + "_" + pdf.get(
                                                                        'title')])


@pdf_annotate_text_bp.route('/pdf/annotate_text', methods=['POST'])
def annotate_text():
    if request.method == 'POST':
        f=request.files['file']
        path=os.path.join(upload_folder, f.filename)
        f.save(path)
        pdf=h.extract_pdf(path)
        body={"document": {
            "type": "PLAIN_TEXT",
            "language": "EN",
            "content": pdf.get('text')
        }, "encodingType": "UTF8",
            'features': {
                "extractSyntax": True,
                "extractEntities": True,
                "extractDocumentSentiment": True,
                "extractEntitySentiment": True,
                "classifyText": True
            }
        }

        response=requests.post(f'{nlp_url}:annotateText'
                               f'?key={api_key}',
                               data=json.dumps(body))
        d=json.loads(response.text)
        print('annotate:' + str(d))
        h.cost_calculator(pdf.get('text'), 'content_classification')
        x=json.dumps(d)
        return render_template('/shared/partials/table.html', data=[json2html.convert(json=x,
                                                                                      table_attributes="id=\"info-table\" class=\"table table-bordered table-hover\""),
                                                                    x,
                                                                    "annotate_text_" + pdf.get(
                                                                        'author') + "_" + pdf.get(
                                                                        'title')])


@pdf_classify_text_bp.route('/pdf/classify_text', methods=['POST'])
def classify_text():
    if request.method == 'POST':
        f=request.files['file']
        path=os.path.join(upload_folder, f.filename)
        f.save(path)
        pdf=h.extract_pdf(path)
        body={"document": {
            "type": "PLAIN_TEXT",
            "language": "EN",
            "content": pdf.get('text')
        }}

        response=requests.post(f'{nlp_url}:classifyText'
                               f'?key={api_key}',
                               data=json.dumps(body))
        d=json.loads(response.text)
        print('classify:' + str(d))
        h.cost_calculator(pdf.get('text'), 'content_classification')
        x=json.dumps(d)
        return render_template('/shared/partials/table.html/', data=[json2html.convert(json=x,
                                                                                      table_attributes="id=\"info-table\" class=\"table table-bordered table-hover\""),
                                                                    x,
                                                                    "classify_text_" + pdf.get(
                                                                        'author') + "_" + pdf.get(
                                                                        'title')])
