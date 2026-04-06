import os
from flask import Flask, render_template, redirect, request
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from backend.database import db_session, default_data
from backend.database.models.users_model import UserModel
from backend.database.models.requests_model import ClientRequestModel
from backend.database.models.booking_model import BookingModel
from backend.forms.auth_forms import LoginForm, RegisterForm
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['SECRET_KEY'] = 'urist_super_secret_key'
app.config['UPLOAD_FOLDER'] = os.path.join('static', 'uploads')

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.get(UserModel, user_id)

@app.context_processor
def inject_user():
    return dict(current_user=current_user)

@app.route('/')
def index():
    lawyers = []
    if current_user.is_authenticated:
        db_sess = db_session.create_session()
        lawyers = db_sess.query(UserModel).filter(UserModel.role == 'lawyer').all()
    return render_template('index.html', lawyers=lawyers)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect('/')
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(UserModel).filter(UserModel.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect('/')
        return render_template('login.html', message="Неправильный логин или пароль", form=form)
    return render_template('login.html', title='Вход', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect('/')
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация', form=form, message="Пароли не совпадают")
        
        db_sess = db_session.create_session()
        if db_sess.query(UserModel).filter(UserModel.email == form.email.data).first():
            return render_template('register.html', title='Регистрация', form=form, message="Такой пользователь уже есть")
        
        user = UserModel(
            name=form.name.data,
            email=form.email.data,
            about=form.about.data,
            role=form.role.data
        )
        user.set_password(form.password.data)

        if form.experience_photo.data:
            f = form.experience_photo.data
            filename = secure_filename(f.filename)
            if not os.path.exists(app.config['UPLOAD_FOLDER']):
                os.makedirs(app.config['UPLOAD_FOLDER'])
            f.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            user.experience_photo = filename

        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/')

@app.route('/clients_department')
@login_required
def clients_department():
    if current_user.role != 'admin':
        return redirect('/')
    db_sess = db_session.create_session()
    # Показываем все заявки для тестирования
    bookings = db_sess.query(BookingModel).all()
    return render_template('clients_department.html', title='Отдел клиентов', bookings=bookings)

@app.route('/lawyer/<int:lawyer_id>', methods=['GET', 'POST'])
@login_required
def lawyer_profile(lawyer_id):
    db_sess = db_session.create_session()
    lawyer = db_sess.get(UserModel, lawyer_id)
    if not lawyer or lawyer.role != 'lawyer':
        return redirect('/')

    slots = [f"{str(h).zfill(2)}:{str(m).zfill(2)}" for h in range(9, 19) for m in (0, 30) if not (h == 18 and m == 30)]

    bookings = db_sess.query(BookingModel).filter(BookingModel.lawyer_id == lawyer_id).all()
    booked_times = [b.time for b in bookings if b.status != 'Отклонено']
    
    can_book = current_user.role in ['client', 'admin']
    
    message = None
    if request.method == 'POST' and can_book:
        time = request.form.get('time')
        problem = request.form.get('problem')
        if time and problem:
            if time in booked_times:
                message = "Это время уже занято, выберите другое!"
            else:
                booking = BookingModel(
                    client_id=current_user.id,
                    lawyer_id=lawyer.id,
                    date="Завтра",
                    time=time,
                    problem=problem,
                    status="В ожидании"
                )
                db_sess.add(booking)
                db_sess.commit()
                message = "✅ Ваша заявка успешно отправлена!"
                booked_times.append(time)
    
    return render_template('lawyer_profile.html', lawyer=lawyer, slots=slots, booked_times=booked_times, message=message, can_book=can_book)

@app.route('/booking_action/<int:booking_id>/<action>', methods=['POST'])
@login_required
def booking_action(booking_id, action):
    if current_user.role != 'admin':
        return redirect('/')
    db_sess = db_session.create_session()
    booking = db_sess.get(BookingModel, booking_id)
    if booking:
        if action == 'accept':
            booking.status = 'Принято'
        elif action == 'reject':
            booking.status = 'Отклонено'
        db_sess.commit()
    return redirect('/clients_department')

def main():
    if not os.path.exists('data'):
        os.makedirs('data')
    db_session.global_init("data/urist.sqlite")
    default_data.default_data()

if __name__ == '__main__':
    main()
    app.run(debug=True, port=5000)
