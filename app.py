import csv

from flask import Flask, render_template, Response
from flask_restful import Api, reqparse
from endpoints import pdf, raw
import logging
import json

logging.basicConfig(filename='./app.log', encoding='utf-8')


app = Flask(__name__)
api = Api(app)
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
    return render_template('index.html')


@app.route('/json2table')
def json2table():
    return render_template('json2table.html')


@app.route('/json2csv', methods=['POST'])
def json2csv():
    parser=reqparse.RequestParser()
    parser.add_argument('name', required=True)
    parser.add_argument('json', required=True)  # add args
    args=parser.parse_args()
    j = json.loads(args.get('json'))
    data_file=open('data.csv', 'w')
    csv_writer=csv.writer(data_file)
    count=0
    for x in j.keys():
        if count == 0:
            csv_writer.writerow(x)
            count+=1
    return Response(
        data_file,
        mimetype="text/csv",
        headers={"Content-disposition":
                     f"attachment; filename={args.get('name')}"})


if __name__ == '__main__':
    app.run(debug=True)
