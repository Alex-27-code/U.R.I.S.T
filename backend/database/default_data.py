import os
from backend.database import db_session
from backend.database.models.users_model import UserModel

def default_data():
    db_sess = db_session.create_session()
    
    # Check if we already have users
    if db_sess.query(UserModel).first():
        return
        
    lawyer1 = UserModel(
        name="Юрист Тестовый 1",
        email="test1@lawyer.ru",
        about="Специалист по семейным делам. Быстро и надежно.",
        role="worker"
    )
    lawyer1.set_password("123")
    
    lawyer2 = UserModel(
        name="Юрист Тестовый 2",
        email="test2@lawyer.ru",
        about="Корпоративный юрист. 10 лет опыта в арбитраже.",
        role="worker"
    )
    lawyer2.set_password("123")
    
    admin = UserModel(
        name="Администратор",
        email="admin@mail.ru",
        about="Владелец портала.",
        role="worker"
    )
    admin.set_password("admin")

    db_sess.add_all([lawyer1, lawyer2, admin])
    db_sess.commit()
