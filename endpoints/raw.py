import requests
from config import api_key
import json
from flask_restful import reqparse
from flask import Blueprint
from helpers import Helpers, nlp_url

h = Helpers()
analyze_entities_endpoint = Blueprint('analyze_entities', __name__)
analyze_entity_sentiment_endpoint = Blueprint('analyze_entity_sentiment', __name__)


@analyze_entities_endpoint.route('/analyze_entities', methods=['POST'])
def analyze_entities():
    parser=reqparse.RequestParser()
    parser.add_argument('text', required=True)  # add args
    args=parser.parse_args()
    body={ "document": {
            "type": "PLAIN_TEXT",
            "language": "EN",
            "content": args.get('text')
        },    "encodingType": "UTF8"}

    response=requests.post(f'{nlp_url}:analyzeEntities'
                           f'?key={api_key}',
                           data=json.dumps(body))
    d=json.loads(response.text)
    h.cost_calculator(args.get('text'), 'entity')
    return json.dumps({'text': args.get('text'),
                       'entities': [d.get('entities')[i].get('name') for i, x in enumerate(d.get('entities'))]})


@analyze_entities_endpoint.route('/analyze_entity_sentiment', methods=['POST'])
def analyze_entity_sentiment():
    parser=reqparse.RequestParser()
    parser.add_argument('text', required=True)  # add args
    args=parser.parse_args()
    body={ "document": {
            "type": "PLAIN_TEXT",
            "language": "EN",
            "content": args.get('text')
        },    "encodingType": "UTF8"}

    response=requests.post(f'{nlp_url}:analyzeEntitySentiment'
                           f'?key={api_key}',
                           data=json.dumps(body))
    d=json.loads(response.text)
    print(d)
    h.cost_calculator(args.get('text'), 'entity_sentiment')
    return json.dumps([d.get('entities')[i].get('name') for i, x in enumerate(d.get('entities'))])


