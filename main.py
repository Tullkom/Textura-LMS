from flask import Flask, render_template, redirect, url_for, flash

import forms
from data import db_session
from data.users import User

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


def main():
    db_session.global_init("db/users.db")
    db_session.create_session()

    app.run()


@app.route('/')
def home():
    return render_template('main.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = forms.LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.username == form.username.data).first()
        if user and user.hashed_password == form.password.data:
            flash('Вы успешно вошли!', 'success')
            return redirect(url_for('success'))
        else:
            flash('Неверное имя пользователя или пароль.', 'danger')
            return render_template('login.html', form=form, title='Авторизация', error='invalid_user')
    return render_template('login.html', form=form, title='Авторизация')


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = forms.RegistrationForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.username == form.username.data).first():
            flash('Пользователь с таким именем уже существует.', 'danger')
        else:
            new_user = User(username=form.username.data, hashed_password=form.password.data)
            db_sess.add(new_user)
            db_sess.commit()
            flash('Вы успешно зарегистрировались!', 'success')
            return redirect(url_for('login'))
    return render_template('register.html', form=form, title='Регистрация')

@app.route('/success')
def success():
    return render_template('success.html')

if __name__ == '__main__':
    main()