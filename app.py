from flask import Flask, render_template
from flask_restful import Api
from endpoints import pdf, raw
import logging

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


if __name__ == '__main__':
    app.run()
