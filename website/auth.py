from flask import Blueprint, render_template, request, flash, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user

from . import db
from .models import User

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Login successful', 'success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
        flash('Incorrect email or password', 'error')

    return render_template("login.html")

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out', 'success')
    return redirect(url_for('auth.login'))

@auth.route('/sign-up', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('firstName')
        password = request.form.get('password1')
        confirm_password = request.form.get('password2')

        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already registered', 'error')
        elif len(email) < 4:
            flash('Email is too short', 'error')
        elif len(first_name) < 2:
            flash('First name is too short', 'error')
        elif password != confirm_password:
            flash('Passwords do not match', 'error')
        elif len(password) < 6:
            flash('Password is too short', 'error')
        else:
            new_user = User(email=email,
                            first_name=first_name,
                            password=generate_password_hash(password, method='pbkdf2:sha256'))
            db.session.add(new_user)
            db.session.commit()
            flash('Account created!', 'success')
            login_user(user, remember=True)
            return redirect(url_for('views.home'))

    return render_template("signup.html")