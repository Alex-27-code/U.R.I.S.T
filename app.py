import datetime
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from flask import Flask, render_template, redirect, request, flash, url_for, session, g
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from flask_wtf import FlaskForm
from flask_wtf.csrf import CSRFProtect
from wtforms import PasswordField, StringField, TextAreaField, SubmitField, EmailField, BooleanField, SelectField, FileField
from wtforms.validators import DataRequired, Email, Optional
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from backend.database import global_init, create_session, SqlAlchemyBase
from backend.database.models.users_model import UserModel
from backend.database.models.booking_model import BookingModel
from backend.database.models.settings_model import SettingsModel
from config import SECRET_KEY, UPLOAD_FOLDER, MAIL_USER, MAIL_PASS, MAIL_TO
import sqlalchemy as sa
import sqlalchemy.orm as orm
from sqlalchemy.exc import IntegrityError

app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

CSRFProtect(app)


def _db():
    if 'db' not in g:
        g.db = create_session()
    return g.db


@app.teardown_appcontext
def _close_db(exc):
    db = g.pop('db', None)
    if db is not None:
        db.close()


login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


@login_manager.unauthorized_handler
def unauthorized():
    from flask import redirect, flash
    flash('Войдите для доступа', 'warning')
    return redirect('/login')


@login_manager.user_loader
def load_user(user_id):
    return _db().get(UserModel, int(user_id))


class LoginForm(FlaskForm):
    email = EmailField('Почта', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')


class RegisterForm(FlaskForm):
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
    photo = FileField('Фото профиля', validators=[Optional()])
    submit = SubmitField('Зарегистрироваться')


class ProfileForm(FlaskForm):
    name = StringField('ФИО', validators=[DataRequired()])
    specialty = StringField('Специализация', validators=[Optional()])
    about = TextAreaField('О себе', validators=[Optional()])
    experience = StringField('Опыт работы', validators=[Optional()])
    price = StringField('Стоимость консультации', validators=[Optional()])
    schedule = StringField('Удобное время', validators=[Optional()])
    photo = FileField('Фото профиля', validators=[Optional()])
    submit = SubmitField('Сохранить')


@app.errorhandler(400)
def error_400(e):
    return render_template('error.html', error_code=400, error_title='Неверный запрос',
                           error_message='Сервер не смог обработать запрос. Проверьте правильность введённых данных.'), 400


@app.errorhandler(403)
def error_403(e):
    return render_template('error.html', error_code=403, error_title='Доступ запрещён',
                           error_message='У вас нет прав для просмотра этой страницы.'), 403


@app.errorhandler(404)
def error_404(e):
    return render_template('error.html', error_code=404, error_title='Страница не найдена',
                           error_message='Запрашиваемая страница не существует или была удалена.'), 404


@app.errorhandler(500)
def error_500(e):
    return render_template('error.html', error_code=500, error_title='Ошибка сервера',
                           error_message='Произошла внутренняя ошибка сервера. Попробуйте позже.'), 500


@app.errorhandler(503)
def error_503(e):
    return render_template('error.html', error_code=503, error_title='Сервис недоступен',
                           error_message='Сервер временно недоступен. Попробуйте зайти позже.'), 503


@app.route('/')
def index():
    db_sess = _db()
    lawyers = []
    settings = db_sess.get(SettingsModel, 1)
    if current_user.is_authenticated:
        lawyers = db_sess.query(UserModel).filter(UserModel.role == 'lawyer').all()
    feedback_sent = session.pop('_feedback_ok', False)
    feedback_error = session.pop('_feedback_error', None)
    return render_template('index.html', lawyers=lawyers, settings=settings,
                           feedback_sent=feedback_sent, feedback_error=feedback_error)


@app.route('/feedback', methods=['POST'])
def feedback():
    sender_name = request.form.get('sender_name', '').strip()
    sender_email = request.form.get('sender_email', '').strip()
    message = request.form.get('message', '').strip()

    if not sender_name or not sender_email or not message:
        session['_feedback_error'] = 'Пожалуйста, заполните все поля.'
        return redirect('/#contacts-section')

    if MAIL_USER and MAIL_PASS:
        try:
            msg = MIMEMultipart()
            msg['From'] = MAIL_USER
            msg['To'] = MAIL_TO
            msg['Subject'] = f'Обратная связь Ю.Р.И.С.Т. от {sender_name}'
            body = f'Имя: {sender_name}\nEmail: {sender_email}\n\nСообщение:\n{message}'
            msg.attach(MIMEText(body, 'plain', 'utf-8'))
            with smtplib.SMTP_SSL('smtp.yandex.ru', 465) as server:
                server.login(MAIL_USER, MAIL_PASS)
                server.sendmail(MAIL_USER, MAIL_TO, msg.as_string())
        except Exception:
            pass

    session['_feedback_ok'] = True
    return redirect('/#contacts-section')



@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect('/')
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = _db()
        user = db_sess.query(UserModel).filter(UserModel.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect('/')
        return render_template('login.html', form=form, message='Неправильный логин или пароль')
    return render_template('login.html', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect('/')
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', form=form, message='Пароли не совпадают')
        db_sess = _db()
        if db_sess.query(UserModel).filter(UserModel.email == form.email.data).first():
            return render_template('register.html', form=form, message='Пользователь с такой почтой уже существует')
        user = UserModel(
            name=form.name.data,
            email=form.email.data,
            role=form.role.data,
            specialty=form.specialty.data or '',
            experience=form.experience.data or '',
            price=form.price.data or '',
            schedule=form.schedule.data or '',
            about=form.about.data or '',
        )
        if form.photo.data and form.photo.data.filename:
            f = form.photo.data
            filename = secure_filename(f.filename)
            if filename:
                f.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                user.photo = filename
        user.set_password(form.password.data)
        db_sess.add(user)
        try:
            db_sess.commit()
        except IntegrityError:
            db_sess.rollback()
            return render_template('register.html', form=form, message='Пользователь с такой почтой уже существует')
        return redirect('/login')
    return render_template('register.html', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/')


@app.route('/lawyer/<int:lawyer_id>', methods=['GET', 'POST'])
@login_required
def lawyer_profile(lawyer_id):
    db_sess = _db()
    lawyer = db_sess.get(UserModel, lawyer_id)
    if not lawyer or lawyer.role != 'lawyer':
        return redirect('/')
    slots = [f"{str(h).zfill(2)}:{str(m).zfill(2)}" for h in range(9, 19) for m in (0, 30) if not (h == 18 and m == 30)]

    def load_booked():
        bks = db_sess.query(BookingModel).filter(BookingModel.lawyer_id == lawyer_id).all()
        result = {}
        for b in bks:
            if b.status != 'rejected' and b.date:
                result.setdefault(b.date, []).append(b.time)
        return result

    message = None
    if request.method == 'POST' and current_user.role == 'client':
        time_val = request.form.get('time')
        problem = request.form.get('problem')
        date = request.form.get('date')
        booked_slots = load_booked()
        if time_val and problem and time_val not in booked_slots.get(date, []):
            booking = BookingModel(
                client_id=current_user.id, lawyer_id=lawyer.id,
                date=date or '', time=time_val, problem=problem, status='pending'
            )
            db_sess.add(booking)
            db_sess.commit()
            # PRG: redirect keeps date in URL so F5 shows the correct date
            return redirect(url_for('lawyer_profile', lawyer_id=lawyer_id, date=date, booked='1'))
        elif time_val in booked_slots.get(date, []):
            message = 'Это время уже занято.'
    else:
        booked_slots = load_booked()

    # Date priority: query param (from PRG redirect) → form → today
    selected_date = request.args.get('date') or request.form.get('date') or datetime.date.today().isoformat()
    if request.args.get('booked'):
        message = 'Заявка отправлена! Ожидайте подтверждения.'

    return render_template(
        'lawyer_profile.html', lawyer=lawyer, slots=slots,
        booked_slots=booked_slots, selected_date=selected_date,
        message=message, can_book=(current_user.role == 'client'),
        min_date=datetime.date.today().isoformat()
    )


@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    if current_user.role != 'lawyer':
        return redirect('/')
    form = ProfileForm()
    if form.validate_on_submit():
        db_sess = _db()
        user = db_sess.get(UserModel, current_user.id)
        user.name = form.name.data
        user.specialty = form.specialty.data or ''
        user.about = form.about.data or ''
        user.experience = form.experience.data or ''
        user.price = form.price.data or ''
        user.schedule = form.schedule.data or ''
        if form.photo.data:
            filename = secure_filename(form.photo.data.filename)
            form.photo.data.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            user.photo = filename
        db_sess.commit()
        flash('Профиль обновлён', 'success')
        return redirect('/')
    form.name.data = current_user.name
    form.specialty.data = current_user.specialty or ''
    form.about.data = current_user.about or ''
    form.experience.data = current_user.experience or ''
    form.price.data = current_user.price or ''
    form.schedule.data = current_user.schedule or ''
    return render_template('profile.html', form=form)


@app.route('/clients_department', methods=['GET', 'POST'])
@login_required
def clients_department():
    if current_user.role != 'admin':
        return redirect('/')
    db_sess = _db()
    bookings = db_sess.query(BookingModel).options(
        orm.joinedload(BookingModel.client),
        orm.joinedload(BookingModel.lawyer),
    ).order_by(BookingModel.id.desc()).all()
    return render_template('clients_department.html', bookings=bookings)


@app.route('/users', methods=['GET', 'POST'])
@login_required
def users():
    if current_user.role != 'admin':
        return redirect('/')
    db_sess = _db()
    users = db_sess.query(UserModel).all()
    return render_template('admin_users.html', users=users)


@app.route('/booking_action/<int:booking_id>/<action>', methods=['GET', 'POST'])
@login_required
def booking_action(booking_id, action):
    if current_user.role != 'admin':
        return redirect('/')
    db_sess = _db()
    booking = db_sess.get(BookingModel, booking_id)
    if booking:
        if action == 'accept':
            booking.status = 'accepted'
        elif action == 'reject':
            booking.status = 'rejected'
        db_sess.commit()
    return redirect('/clients_department')


@app.route('/admin/settings', methods=['GET', 'POST'])
@login_required
def admin_settings():
    if current_user.role != 'admin':
        return redirect('/')
    db_sess = _db()
    settings = db_sess.get(SettingsModel, 1)
    if not settings:
        settings = SettingsModel(id=1)
        db_sess.add(settings)
        db_sess.commit()
    if request.method == 'POST':
        settings.about_text = request.form.get('about_text', '')
        settings.contact_text = request.form.get('contact_text', '')
        settings.phone = request.form.get('phone', '')
        settings.address = request.form.get('address', '')
        db_sess.commit()
        flash('Настройки сохранены!', 'success')
        return redirect('/admin/settings')
    return render_template('admin_settings.html', settings=settings)


@app.route('/admin/user/<int:user_id>/delete', methods=['GET'])
@login_required
def admin_delete_user(user_id):
    if current_user.role != 'admin':
        return redirect('/')
    db_sess = _db()
    user = db_sess.get(UserModel, user_id)
    if user and user.id != current_user.id:
        db_sess.delete(user)
        db_sess.commit()
    return redirect('/users')


@app.route('/admin/user/<int:user_id>/edit', methods=['GET', 'POST'])
@login_required
def admin_edit_user(user_id):
    if current_user.role != 'admin':
        return redirect('/')
    db_sess = _db()
    user = db_sess.get(UserModel, user_id)
    if not user:
        return redirect('/users')
    if request.method == 'POST':
        user.name = request.form.get('name', '')
        user.specialty = request.form.get('specialty', '')
        user.experience = request.form.get('experience', '')
        user.price = request.form.get('price', '')
        user.schedule = request.form.get('schedule', '')
        user.about = request.form.get('about', '')
        db_sess.commit()
        flash('Профиль обновлён!', 'success')
        return redirect('/users')
    return render_template('admin_edit_user.html', user=user)


@app.route('/admin/booking/<int:booking_id>/delete', methods=['GET'])
@login_required
def admin_delete_booking(booking_id):
    if current_user.role != 'admin':
        return redirect('/')
    db_sess = _db()
    booking = db_sess.get(BookingModel, booking_id)
    if booking:
        db_sess.delete(booking)
        db_sess.commit()
    return redirect('/clients_department')


def start_server():
    import backend.database.default_data as _dd
    from config import DATABASE_PATH, HOST, PORT
    global_init(DATABASE_PATH)
    _dd.default_data()
    app.run(port=PORT, host=HOST, debug=False)


if __name__ == '__main__':
    start_server()