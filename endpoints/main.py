import json
import pandas as pd
from flask import render_template, make_response, Blueprint
from flask_login import login_required, current_user
from flask_restful import reqparse


main=Blueprint('main', __name__)


@main.route('/')
def index():
    return render_template('index.html', title='title', description='description')

@main.route('/contact')
def contact():
    return render_template('shared/partials/contact.html')

@main.route('/pdf')
@login_required
def pdf():
    return render_template('shared/partials/pdf.html')


@main.route('/raw')
@login_required
def raw():
    return render_template('/shared/partials/raw.html')


@main.route('/pricing')
def pricing():
    return render_template('/shared/partials/pricing.html')


@main.route('/download_csv', methods=['POST'])
@login_required
def download_csv():
    parser=reqparse.RequestParser()
    parser.add_argument('name', required=True)
    parser.add_argument('json', required=True)  # add args
    args=parser.parse_args()
    j=json.loads(args.get('json'))
    df=pd.json_normalize(j)
    df=df.to_csv(index=False)
    output=make_response(df)
    output.headers["Content-Disposition"]=f"attachment; filename={args.get('name')}.csv"
    output.headers["Content-type"]="text/csv"
    return output


@main.route('/download_json', methods=['POST'])
@login_required
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



