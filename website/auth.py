from flask import Blueprint, render_template, request, flash, redirect, url_for

from .models import User
from . import db

from werkzeug.security import generate_password_hash, check_password_hash

from flask_login import login_user, login_required, logout_user, current_user


auth = Blueprint('auth', __name__)


@auth.route('/signup', methods=['GET', 'POST'])
def signup():
	if request.method == 'POST':
		email = request.form.get('email')
		firstName = request.form.get('firstName')
		password1 = request.form.get('password1')
		password2 = request.form.get('password2')

		user = User.query.filter_by(email=email).first()
		if user:
			flash('Email already exists.', category='error')

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
			login_user(user, remember=True)
			return redirect(url_for('views.home'))

	return render_template("signup.html")

@auth.route('/login', methods=['GET', 'POST'])
def login():
	if request.method == 'POST':
		email = request.form.get('email')
		password = request.form.get('password')

		user = User.query.filter_by(email=email).first()
		if user:
			if check_password_hash(user.password, password):
				flash('Logged in successfully', category='success')
				login_user(user, remember=True)
				return redirect(url_for('views.home'))
			else:
				flash('Retry password or email.', category='error')
		else:
			flash('Email does not exist.', category='error')

	return render_template("login.html")

@auth.route('/logout')
@login_required
def logout():
	logout_user()
	return redirect(url_for('auth.login'))