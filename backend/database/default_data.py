import os
from backend.database import db_session
from backend.database.models.users_model import UserModel

def default_data():
    db_sess = db_session.create_session()
    
    # Check if we already have users
    if db_sess.query(UserModel).first():
        return
        
    lawyer1 = UserModel(
        name="Алексей Смирнов",
        email="smirnov@lawyer.ru",
        about="Опытный юрист по семейному праву. Проведу подробную консультацию.",
        role="lawyer"
    )
    lawyer1.set_password("123")
    
    lawyer2 = UserModel(
        name="Елена Васильева",
        email="vasilyeva@lawyer.ru",
        about="Специалист по гражданским делам. Помогу разобраться с документами.",
        role="lawyer"
    )
    lawyer2.set_password("123")
    
    admin = UserModel(
        name="Администратор",
        email="admin@mail.ru",
        about="Владелец портала.",
        role="admin"
    )
    admin.set_password("admin")

    db_sess.add_all([lawyer1, lawyer2, admin])
    db_sess.commit()
