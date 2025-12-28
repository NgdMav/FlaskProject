from flask import Blueprint, render_template, request, flash

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    return render_template("login.html")

@auth.route('/logout')
def logout():
    return '<p>Logout</p>'

@auth.route('/sign-up', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('firstName')
        password = request.form.get('password1')
        confirm_password = request.form.get('password2')

        if len(email) < 4:
            flash('Email is too short', 'error')
        elif len(first_name) < 2:
            flash('First name is too short', 'error')
        elif password != confirm_password:
            flash('Passwords do not match', 'error')
        elif len(password) < 6:
            flash('Password is too short', 'error')
        else:
            flash('Account created!', 'success')

    return render_template("signup.html")