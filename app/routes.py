from app import app
from flask import render_template, flash, redirect, url_for
from app.forms import LoginForum


@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'Darko'}
    posts = [
        {
            'Author' : {'username': 'Gwyn'},
            'body' : 'Sweet dreams dear prince'
        },
        {
            'Author' : {'username': 'Varok'},
            'body' : 'Honor, young heroes... no matter how dire the battle... never forsake it.'
        },
        {
            'Author' : {'username': 'Murlock'},
            'body' : 'Mglrmglmglmgl!'
        },
    ]
    return render_template('index.html', title="Home", user=user, posts=posts)


@app.route('/feed')
def feed():
    return "ti si feeder!" # da se napravi template

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForum()
    if form.validate_on_submit():
        flash('Login requested for user {}, remember_me={}'.format(
            form.username.data, form.remember_me.data))
        return redirect(url_for('/index'))
    return render_template('login.html', title='Sign In', form=form)

