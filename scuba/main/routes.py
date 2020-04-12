from flask import render_template, url_for, flash, redirect, jsonify
from main import app, db, bcrypt
from main.forms import RegistrationForm, LoginForm
from main.models import User, Post
from flask_login import login_user  # current_user, logout_user


posts = [
    {
        'author': 'Corey Schafer',
        'title': 'Blog Post 1',
        'content': 'First post content',
        'date_posted': 'April 20, 2018'
    },
    {
        'author': 'Jane Doe',
        'title': 'Blog Post 2',
        'content': 'Second post content',
        'date_posted': 'April 21, 2018'
    }
]


@app.route('/layout')
def layout():
    return render_template('layout.html')


@app.route('/trying')
def trying():
    return render_template('trying.html')


@app.route('/', methods=["GET"])
def test():
    return jsonify({'message': 'It Works!'})


languages = [{'name': 'Javascript'}, {'name': 'Python'}, {'name': 'Ruby'}]


@app.route('/lang', methods=['GET'])
def returnAll():
    return jsonify({'languages': languages})


@app.route('/main')
def main():
    return render_template('main.html')


@app.route('/home')
def home():
    return render_template('home.html')


@app.route("/login", methods=['GET', 'POST'])
def login():
    '''if current_user.is_authenticated:
        return redirect(url_for('main'))'''
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            return redirect(url_for('main'))

        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(
            form.password.data).decode('utf-8')
        user = User(username=form.username.data,
                    email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()

        flash(f'Account created for noww!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main'))
