from flask import Blueprint, request, redirect, render_template, url_for, session, flash
from flask_login import login_user, login_required, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy

from  models import User

auth=Blueprint('auth', __name__)


@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email=request.form.get('email')
        name=request.form.get('name')
        password=request.form.get('password')

        user=User.query.filter_by(
            email=email).first()  # if this returns a user, then the email already exists in database

        if user:  # if a user is found, we want to redirect back to signup page so user can try again
            flash('Email address already exists')
            return redirect(url_for('auth.signup'))

        new_user=User(email=email, name=name, password=generate_password_hash(password, method='sha256'))
        db=SQLAlchemy()
        db.session.add(new_user)
        db.session.commit()
        return render_template('/index.html')

    return render_template('/auth/signup.html')


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email=request.form.get('email')
        password=request.form.get('password')
        remember=True if request.form.get('remember') else False

        user=User.query.filter_by(email=email).first()

        if not user or not check_password_hash(user.password, password):
            flash('Please check your login details and try again.')
            return redirect(url_for('auth.login'))  # if user doesn't exist or password is wrong, reload the page

        login_user(user, remember=remember)
        return render_template('/index.html')
    return render_template('/auth/login.html')


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return render_template('/index.html')


# @auth.route('/', methods=['GET'])
# def home():
#     return render_template('index.html', title='title', description='description')
