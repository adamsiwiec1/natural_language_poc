import json

import requests
from flask import Blueprint
from flask_restful import reqparse

from config import api_key
from helpers import Helpers, nlp_url

h=Helpers()
analyze_entities_bp=Blueprint('analyze_entities', __name__)
analyze_entity_sentiment_bp=Blueprint('analyze_entity_sentiment', __name__)
analyze_sentiment_bp=Blueprint('analyze_sentiment', __name__)
analyze_syntax_bp=Blueprint('analyze_syntax', __name__)
annotate_text_bp=Blueprint('annotate_text', __name__)
classify_text_bp=Blueprint('classify_text', __name__)

'''
https://cloud.google.com/natural-language/docs/reference/rest
https://cloud.google.com/natural-language
'''


@analyze_entities_bp.route('/analyze_entities', methods=['POST'])
def analyze_entities():
    parser=reqparse.RequestParser()
    parser.add_argument('text', required=True)  # add args
    args=parser.parse_args()
    body={"document": {
        "type": "PLAIN_TEXT",
        "language": "EN",
        "content": args.get('text')
    }, "encodingType": "UTF8"}

    response=requests.post(f'{nlp_url}:analyzeEntities'
                           f'?key={api_key}',
                           data=json.dumps(body))
    d=json.loads(response.text)
    h.cost_calculator(args.get('text'), 'entity')
    return json.dumps({'text': args.get('text'),
                       'entities': [d.get('entities')[i].get('name') for i, x in enumerate(d.get('entities'))]})


@analyze_entities_bp.route('/analyze_entity_sentiment', methods=['POST'])
def analyze_entity_sentiment():
    parser=reqparse.RequestParser()
    parser.add_argument('text', required=True)  # add args
    args=parser.parse_args()
    body={"document": {
        "type": "PLAIN_TEXT",
        "language": "EN",
        "content": args.get('text')
    }, "encodingType": "UTF8"}

    response=requests.post(f'{nlp_url}:analyzeEntitySentiment'
                           f'?key={api_key}',
                           data=json.dumps(body))
    d=json.loads(response.text)
    print(d)
    h.cost_calculator(args.get('text'), 'entity_sentiment')
    return json.dumps({'text': args.get('text'),
                       'entities': [d.get('entities')[i].get('name') for i, x in enumerate(d.get('entities'))]})


@analyze_sentiment_bp.route('/analyze_sentiment', methods=['POST'])
def analyze_sentiment():
    parser=reqparse.RequestParser()
    parser.add_argument('text', required=True)  # add args
    args=parser.parse_args()
    body={"document": {
        "type": "PLAIN_TEXT",
        "language": "EN",
        "content": args.get('text')
    }, "encodingType": "UTF8"}

    response=requests.post(f'{nlp_url}:analyzeSentiment'
                           f'?key={api_key}',
                           data=json.dumps(body))
    d=json.loads(response.text)
    print('sentiment:' + str(d))
    h.cost_calculator(args.get('text'), 'syntax')
    return json.dumps({'text': args.get('text'),
                       'doc_magnitude': d.get('documentSentiment').get('magnitude'),
                       'doc_score': d.get('documentSentiment').get('score'),
                       'language': d.get('language'),
                       'sentences': d.get('sentences')})


@analyze_syntax_bp.route('/analyze_syntax', methods=['POST'])
def analyze_syntax():
    parser=reqparse.RequestParser()
    parser.add_argument('text', required=True)  # add args
    args=parser.parse_args()
    body={"document": {
        "type": "PLAIN_TEXT",
        "language": "EN",
        "content": args.get('text')
    }, "encodingType": "UTF8"}

    response=requests.post(f'{nlp_url}:analyzeSyntax'
                           f'?key={api_key}',
                           data=json.dumps(body))
    d=json.loads(response.text)
    print('syntax:' + str(d))
    h.cost_calculator(args.get('text'), 'syntax')
    return json.dumps(d)


@annotate_text_bp.route('/annotate_text', methods=['POST'])
def annotate_text():
    parser=reqparse.RequestParser()
    parser.add_argument('text', required=True)  # add args
    args=parser.parse_args()
    body={"document": {
        "type": "PLAIN_TEXT",
        "language": "EN",
        "content": args.get('text')
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
    h.cost_calculator(args.get('text'), 'entity')
    return json.dumps(d)


@classify_text_bp.route('/classify_text', methods=['POST'])
def classify_text():
    parser=reqparse.RequestParser()
    parser.add_argument('text', required=True)  # add args
    args=parser.parse_args()
    body={"document": {
        "type": "PLAIN_TEXT",
        "language": "EN",
        "content": args.get('text')
    }}

    response=requests.post(f'{nlp_url}:classifyText'
                           f'?key={api_key}',
                           data=json.dumps(body))
    d=json.loads(response.text)
    print('classify:' + str(d))
    h.cost_calculator(args.get('text'), 'entity_sentiment')
    return json.dumps(d)
