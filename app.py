import json
import json
import logging

import jinja_partials
import pandas as pd
from flask import Flask, render_template, make_response
from flask_restful import Api, reqparse

from endpoints import pdf, raw

logging.basicConfig(filename='./app.log', encoding='utf-8')

app=Flask(__name__)
api=Api(app)
jinja_partials.register_extensions(app)

app.register_blueprint(pdf.pdf_analyze_entities_bp)
app.register_blueprint(pdf.pdf_analyze_entity_sentiment_bp)
app.register_blueprint(pdf.pdf_analyze_sentiment_bp)
app.register_blueprint(pdf.pdf_analyze_syntax_bp)
app.register_blueprint(pdf.pdf_annotate_text_bp)
app.register_blueprint(pdf.pdf_classify_text_bp)
app.register_blueprint(raw.analyze_entities_bp)
app.register_blueprint(raw.analyze_entity_sentiment_bp)
app.register_blueprint(raw.analyze_sentiment_bp)
app.register_blueprint(raw.analyze_syntax_bp)
app.register_blueprint(raw.annotate_text_bp)
app.register_blueprint(raw.classify_text_bp)


@app.route('/')
def index():
    return render_template('index.html', title='title', description='description')


@app.route('/pdf')
def pdf():
    return render_template('shared/partials/pdf.html')


@app.route('/raw')
def raw():
    return render_template('/shared/partials/raw.html')


@app.route('/download_csv', methods=['POST'])
def download_csv():
    parser=reqparse.RequestParser()
    parser.add_argument('name', required=True)
    parser.add_argument('json', required=True)  # add args
    args=parser.parse_args()
    j=json.loads(args.get('json'))
    print(j)
    df = pd.json_normalize(j)
    print(df)
    df=df.to_csv(index=False)
    output=make_response(df)
    output.headers["Content-Disposition"]=f"attachment; filename={args.get('name')}.csv"
    output.headers["Content-type"]="text/csv"
    return output


@app.route('/download_json', methods=['POST'])
def download_json():
    parser=reqparse.RequestParser()
    parser.add_argument('name', required=True)
    parser.add_argument('json', required=True)  # add args
    args=parser.parse_args()
    j=args.get('json')
    output=make_response(j)
    output.headers["Content-Disposition"]=f"attachment; filename={args.get('name')}.json"
    output.headers["Content-type"]="text/json"
    return output


if __name__ == '__main__':
    app.run(debug=True)
