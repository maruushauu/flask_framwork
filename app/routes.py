from flask import render_template, flash, redirect, url_for, make_response, request, session
from app import app, db
from app.forms import LoginForm, RegistrationForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User
from werkzeug.urls import url_parse
# @app.route('/setcookie')
# def setcookie():
#     resp = make_response(redirect(url_for('index')))
#     resp.set_cookie('flask_cookie', 'cookie_value')
#
#     return resp
#
# @app.route('/getcookie')
# def getcookie():
#     flask_cookie = request.cookies.get('flask_cookie')
#     return '<h1>Cookie: ' + flask_cookie + '</h1>'


# @app.route('/setsession', methods = ['GET', 'POST'])
# def setsession():
#     if request.method == 'POST':
#         session['username'] = request.form['username']
#         return redirect(url_for('index'))
#     return '''
#         <form action="" method="post">
#         <p><input type=text name=username>
#         <p><input type=submit value=Логин>
#     '''

# @app.route('/unsetsession')
# def unsetsession():
#     session.pop('username', None)
#     return redirect(url_for('index'))
#
app.secret_key = 'SOME SECRET'

@app.route('/')
@app.route('/index')
@login_required
def index():
    # if 'username' in session:
    #     return '<h1>Session: %s</h1>' % session['username']
    # return '<h1>No session!</h1>'
    #
    # user = {'username': 'Mary'}
    posts = [
        {
            'author': {'username': 'Mary'},
            'body': 'Привет!'
        },
        {
            'author': {'username': 'Pavel'},
            'body': 'hello!'
        },
        {
            'author': {'username': 'Oly'},
            'body': 'Ура!'
        }
    ]
    return render_template('index.html', title='Домашняя страница', posts=posts )

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm(csrf_enabled=False)
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Неправильный пользователь или пароль!')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Вход', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Ура, вы зарегистрированы!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Регистрация', form=form)