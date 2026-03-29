from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import PasswordField, StringField, TextAreaField, SubmitField, EmailField, BooleanField, SelectField
from wtforms.validators import DataRequired, Email, Optional

class RegisterForm(FlaskForm):
    email = EmailField('Почта', validators=[DataRequired(), Email()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    password_again = PasswordField('Повторите пароль', validators=[DataRequired()])
    name = StringField('Имя пользователя / ФИО', validators=[DataRequired()])
    
    role = SelectField('Кто вы?', choices=[
        ('client', 'Ищу услугу (Клиент)'),
        ('worker', 'Предоставляю услугу (Рабочий)'),
        ('job_seeker', 'Хочу устроиться юристом (Соискатель)')
    ], validators=[DataRequired()])
    
    about = TextAreaField("Немного о себе (обязательно для рабочих и соискателей)", validators=[Optional()])
    experience_photo = FileField('Фото вашего рабочего опыта/диплома', validators=[
        Optional(), 
        FileAllowed(['jpg', 'png', 'jpeg'], 'Только изображения!')
    ])
    
    submit = SubmitField('Зарегистрироваться')

class LoginForm(FlaskForm):
    email = EmailField('Почта', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')
