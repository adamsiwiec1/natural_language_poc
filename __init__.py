# comment these next two lines out for production
# import local_config as lc
# lc.set_env_vars()
from flask import Flask, render_template,url_for
from flask_login import LoginManager
from auth import auth as auth_blueprint
from endpoints.main import main as main_blueprint
from endpoints.pdf import pdf as pdf_blueprint
from endpoints.raw import raw as raw_blueprint
from models import User,init_db
import os


app=Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


# these are uploaded as ENV var in the cloud run instance
SQL_USER = os.environ['SQL_USER']
SQL_PASSWORD = os.environ['SQL_PASSWORD']
SQL_IPV4 = os.environ['SQL_IPV4']
SQL_DB = os.environ['SQL_DB']
app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{SQL_USER}:{SQL_PASSWORD}@{SQL_IPV4}/{SQL_DB}'

init_db(app)

login_manager=LoginManager()
login_manager.login_view='auth.login'
login_manager.init_app(app)

app.register_blueprint(auth_blueprint)
app.register_blueprint(main_blueprint)
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