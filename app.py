from flask import Flask, render_template
from flask_restful import Api
from endpoints import pdf, raw
import logging

logging.basicConfig(filename='./app.log', encoding='utf-8')


app = Flask(__name__)
api = Api(app)
app.register_blueprint(pdf.pdf_analyze_entities_endpoint)
app.register_blueprint(pdf.pdf_analyze_entity_sentiment_endpoint)
app.register_blueprint(raw.analyze_entities_endpoint)
app.register_blueprint(raw.analyze_entity_sentiment_endpoint)


@app.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    app.run()
