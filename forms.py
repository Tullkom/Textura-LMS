from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms import TextAreaField, FileField
from wtforms.validators import DataRequired, EqualTo


class LoginForm(FlaskForm):
    username = StringField('Имя пользователя', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')

class RegistrationForm(FlaskForm):
    username = StringField('Имя пользователя', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    confirm_password = PasswordField(
        'Подтвердите пароль',
        validators=[DataRequired(), EqualTo('password', message='Пароли должны совпадать')]
    )
    submit = SubmitField('Зарегистрироваться')

class AddBookForm(FlaskForm):
    title = StringField('Название книги', validators=[DataRequired()])
    content = TextAreaField("О книге")
    is_private = BooleanField("Недоступно гостям")
    file = FileField("Текст книги в формате .txt", validators=[DataRequired()])
    submit = SubmitField('Выложить')

class EditBookForm(FlaskForm):
    content = TextAreaField("О книге")
    is_private = BooleanField("Недоступно гостям")
    submit = SubmitField('Применить')

class DeleteBookForm(FlaskForm):
    submit = SubmitField('Удалить')

class SearchForm(FlaskForm):
    query = StringField('Название книги', validators=[DataRequired()])
    submit = SubmitField('Поиск')