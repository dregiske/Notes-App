from flask import Blueprint, render_template, request, flash, redirect, url_for

from .models import User
from . import db

from werkzeug.security import generate_password_hash, check_password_hash


auth = Blueprint('auth', __name__)


@auth.route('/signup', methods=['GET', 'POST'])
def signup():
	if request.method == 'POST':
		email = request.form.get('email')
		firstName = request.form.get('firstName')
		password1 = request.form.get('password1')
		password2 = request.form.get('password2')

		if len(email) < 4:
			flash('Email must be greater than 4 characters.', category='error')
		if len(firstName) < 2:
			flash('First name must be greater than 1 character.', category='error')
		if password1 != password2:
			flash('Passwords don\'t match.', category='error')
		if len(password1) < 7:
			flash('Password must be at least 7 characters long.', category='error')
		else:
			hashed_password = generate_password_hash(password1, method='scrypt')
			new_user = User(email=email,
							password=hashed_password,
							first_name=firstName,
			)
			db.session.add(new_user)
			db.session.commit()

			flash('Accounted created.', category='success')
			return redirect(url_for('views.home'))

	return render_template("signup.html")

@auth.route('/login', methods=['GET', 'POST'])
def login():
	return render_template("login.html")

@auth.route('/logout')
def logout():
	return "<p>Logout</p>"