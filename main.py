from flask import Flask, render_template, redirect, url_for, flash
from flask import send_file
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from forms import LoginForm, RegistrationForm, BookForm
from sqlalchemy import and_
from data import db_session
from data.users import User
from data.books import Book
from json import loads
import os


app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
app.config['UPLOAD_FOLDER'] = 'uploads'

login_manager = LoginManager()
login_manager.init_app(app)

def main():
    db_session.global_init("db/users.db")
    app.run()


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/')
def home():
    return render_template('main.html', title='Текстура')

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        if form.password.data != form.confirm_password.data:
            return render_template('register.html', form=form, title='Регистрация', error='diff_pass')
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.username == form.username.data).first():
            return render_template('register.html', form=form, title='Регистрация', error='existing_user')
        new_user = User(username=form.username.data)
        new_user.set_password(form.password.data)
        db_sess.add(new_user)
        db_sess.commit()
        flash('Вы успешно зарегистрировались!', 'success')
        return redirect('/')
    return render_template('register.html', form=form, title='Регистрация')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.username == form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            flash('Вы успешно вошли!', 'success')
            return redirect(url_for('success'))
        flash('Неверное имя пользователя или пароль.', 'danger')
        return render_template('login.html', form=form, title='Авторизация', error='invalid_user')
    return render_template('login.html', form=form, title='Авторизация')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")

@app.route('/success', methods=['GET', 'POST'])
def success():
    return render_template('success.html')

@app.route('/popular', methods=['GET', 'POST'])
def popular():
    return render_template('popular.html', title='Популярное')

@app.route('/newest', methods=['GET', 'POST'])
def newest():
    db_sess = db_session.create_session()
    if current_user.is_authenticated:
        books = db_sess.query(Book).order_by(Book.id)[::-1]
    else:
        books = db_sess.query(Book).filter(Book.is_private == False).order_by(Book.id)[::-1]
    return render_template('newest.html', books=books, title='Новинки')

@app.route('/faq', methods=['GET', 'POST'])
def faq():
    return render_template('faq.html', title='FAQ')

@app.route('/about', methods=['GET', 'POST'])
def about():
    return render_template('about.html', title='О нас')

@app.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    return render_template('account.html', title=current_user.username)

@app.route('/add_book',  methods=['GET', 'POST'])
@login_required
def add_book():
    form = BookForm()
    if form.validate_on_submit():
        uploaded_file = form.file.data
        filename = current_user.username + '_' + form.title.data + '.txt'
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        uploaded_file.save(file_path)

        db_sess = db_session.create_session()
        book = Book()
        book.title = form.title.data
        book.about = form.content.data
        book.is_private = form.is_private.data
        book.path = '/uploads/' + current_user.username + '_' + book.title.replace(' ', '_') + '.txt'
        current_user.books.append(book)
        db_sess.merge(current_user)
        db_sess.commit()

        return redirect('/')
    return render_template('add_book.html', title='Добавление книги',
                           form=form)


def has_viewed(book, user):
    return user and any(v.id == user.id for v in book.viewers)


@app.route('/book_page/<string:author>/<string:book_name>', methods=['GET', 'POST'])
def book_page(author, book_name):
    book_name = book_name.replace('_', ' ')
    db_sess = db_session.create_session()
    uid = db_sess.query(User).filter(User.username == author).first().id
    book = db_sess.query(Book).filter(and_(Book.user_id == uid, Book.title == book_name)).first()

    if current_user.is_authenticated and not has_viewed(book, current_user):
        book.views += 1
        viewer = db_sess.query(User).get(current_user.id)
        book.viewers.append(viewer)
        db_sess.commit()

    return render_template('book.html',
                           title=book.title + ' - ' + book.user.username,
                           book_name=book.title,
                           author=author,
                           about=book.about,
                           views=book.views)

@app.route('/download/<string:author>/<string:book_name>',  methods=['GET', 'POST'])
def download(author, book_name):
    path = os.path.join(app.config['UPLOAD_FOLDER'], author + '_' + book_name + '.txt')
    return send_file(path, as_attachment=True)

@app.route('/read/<string:author>/<string:book_name>/<int:page>',  methods=['GET', 'POST'])
def read(author, book_name, page):
    book_title = book_name.replace('_', ' ')
    path = os.path.join(app.config['UPLOAD_FOLDER'], author + '_' + book_name + '.txt')
    f = open(path, mode='r', encoding='utf8')
    content = f.read()
    last_page = len(content)//2000 + 1
    content = content[2000 * (page - 1): 2000 * page] + ' -->'
    f.close()
    return render_template('read.html', title=book_title + ' - ' + author,
                           book_name=book_title, author=author, page=page,
                           content=content, last_page=last_page)

@app.route('/down')
def download_file():
    path = 'file.txt'
    return send_file(path, as_attachment=True)

if __name__ == '__main__':
    main()