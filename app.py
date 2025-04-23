from flask import Flask, render_template, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from forms import LoginForm, RegistrationForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)


    def __repr__(self):
        return f'<User {self.username}>'


@app.route('/')
def home():
    return render_template('base.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.password == form.password.data:
            flash('Вы успешно вошли!', 'success')
            return redirect(url_for('success'))
        else:
            flash('Неверное имя пользователя или пароль.', 'danger')
    return render_template('login.html', form=form, title='Авторизация')

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        if User.query.filter_by(username=form.username.data).first():
            flash('Пользователь с таким именем уже существует.', 'danger')
        else:
            new_user = User(username=form.username.data, password=form.password.data)
            db.session.add(new_user)
            db.session.commit()
            flash('Вы успешно зарегистрировались!', 'success')
            return redirect(url_for('login'))
    return render_template('register.html', form=form, title='Регистрация')

@app.route('/success')
def success():
    return render_template('success.html')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)