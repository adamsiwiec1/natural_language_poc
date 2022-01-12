import logging

from flask import Flask, render_template
from flask_login import LoginManager

from auth import auth as auth_blueprint
from endpoints.error import error as error_blueprint
from endpoints.main import main as main_blueprint
from endpoints.pdf import pdf as pdf_blueprint
from endpoints.raw import raw as raw_blueprint
from models import User,init_db
import os

print('WTF')

app=Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
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


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))