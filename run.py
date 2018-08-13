'''
Created on Aug 9, 2018

@author: Yan
'''

from datetime import datetime
from flask import Flask, render_template, url_for, flash, redirect
from flask_sqlalchemy import SQLAlchemy, Model
from app.forms import registrationform, loginform
from flask_wtf import form

stack = Flask(__name__)
stack.config['SECRET_KEY'] = '91d266c6baa55b103f3a2a71fb35a740'
stack.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(stack)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False,
                           default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True)

    def __repr__(self):
        return f"user('{self.username}, {self.email}, {self.image_file}')"


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(90), nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"user('{self.title}, {self.date}')"


posts = [
    {
        'user': 'kaime mzii',
        'title': 'blog post 1',
        'content': 'fitst post content',
        'date': 'april 20, 2018'
    },
    {
        'user': 'dope mkali',
        'title': 'blog post 2',
        'content': 'second post content',
        'date': 'april 20, 2018'
    }
]


@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html', posts=posts)


@app.route("/register", methods=['GET', 'POST'])
def register():
    form = registrationform()
    if form.validate_on_submit():
        flash(f'Account created for {form.username.data}!')
        return redirect(url_for('home'))
    return render_template('register.html', title='Registration Page', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    form = loginform()
    if form.validate_on_submit():
        if form.email.data == 'admin@site.com' and form.password.data == 'password':
            flash('you have been logged in!')
            return redirect(url_for('home'))
        else:
            flash('Login unsuccessful. Please check your details')
    return render_template('login.html', title='Login Page', form=form)


if __name__ == '__name__':
    app.run(debug=True)
