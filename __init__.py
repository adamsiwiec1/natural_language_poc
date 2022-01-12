import logging

from flask import Flask, render_template
from flask_login import LoginManager


from auth import auth as auth_blueprint
from endpoints.error import error as error_blueprint
from endpoints.main import main as main_blueprint
from endpoints.pdf import pdf as pdf_blueprint
from endpoints.raw import raw as raw_blueprint
from models import User,init_db
from waitress import serve


# init SQLAlchemy so we can use it later in our models


logging.basicConfig(filename='../app.log', encoding='utf-8')

app=Flask(__name__)

app.config['SECRET_KEY']='secret-key-goes-here'
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///db.sqlite'
init_db(app)

login_manager=LoginManager()
login_manager.login_view='auth.login'
login_manager.init_app(app)

app.register_blueprint(auth_blueprint)
app.register_blueprint(main_blueprint)
app.register_blueprint(error_blueprint)
app.register_blueprint(pdf_blueprint)
app.register_blueprint(raw_blueprint)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.errorhandler(404)
def page_not_found(error):
    return render_template('/shared/partials/page_not_found.html'), 404


def main():
    serve(app,host='0.0.0.0', port=5000)
