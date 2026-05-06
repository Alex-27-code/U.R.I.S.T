"""Forms for authentication and profile management.
All WTForms classes are centralized here to avoid duplication in app.py.
"""
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import (
    PasswordField, StringField, TextAreaField,
    SubmitField, EmailField, BooleanField, SelectField,
)
from wtforms.validators import DataRequired, Email, Optional


class LoginForm(FlaskForm):
    """Форма входа в систему."""
    email = EmailField('Почта', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')


class RegisterForm(FlaskForm):
    """Registration form for a new user."""
    name = StringField('ФИО', validators=[DataRequired()])
    email = EmailField('Почта', validators=[DataRequired(), Email()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    password_again = PasswordField('Повторите пароль', validators=[DataRequired()])
    role = SelectField('Тип аккаунта', choices=[
        ('client', 'Клиент — ищу юриста'),
        ('lawyer', 'Юрист — предоставляю услуги'),
    ], validators=[DataRequired()])
    specialty = StringField('Специализация', validators=[Optional()])
    experience = StringField('Опыт работы', validators=[Optional()])
    price = StringField('Стоимость', validators=[Optional()])
    schedule = StringField('График работы', validators=[Optional()])
    about = TextAreaField('О себе', validators=[Optional()])
    photo = FileField('Фото профиля', validators=[
        Optional(),
        FileAllowed(['jpg', 'png', 'jpeg'], 'Только изображения'),
    ])
    submit = SubmitField('Зарегистрироваться')

    def validate_password_again(self, field):
        if field.data != self.password.data:
            raise ValidationError('Пароли не совпадают')


class ProfileForm(FlaskForm):
    """Форма редактирования профиля юриста."""
    name = StringField('ФИО', validators=[DataRequired()])
    specialty = StringField('Специализация', validators=[Optional()])
    about = TextAreaField('О себе', validators=[Optional()])
    experience = StringField('Опыт работы', validators=[Optional()])
    price = StringField('Стоимость консультации', validators=[Optional()])
    schedule = StringField('Удобное время', validators=[Optional()])
    photo = FileField('Фото профиля', validators=[
        Optional(),
        FileAllowed(['jpg', 'png', 'jpeg'], 'Только изображения'),
    ])
    submit = SubmitField('Сохранить')