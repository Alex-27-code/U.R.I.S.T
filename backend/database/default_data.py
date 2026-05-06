from backend.database import create_session
from backend.database.models.users_model import UserModel
from backend.database.models.settings_model import SettingsModel


def default_data():
    db_sess = create_session()

    if not db_sess.query(UserModel).filter(UserModel.email == "admin@urist.ru").first():
        admin = UserModel()
        admin.email = "admin@urist.ru"
        admin.name = "Администратор"
        admin.set_password("Admin2024!")
        admin.role = "admin"
        db_sess.add(admin)

    if not db_sess.query(UserModel).filter(UserModel.email == "smirnov@lawyer.ru").first():
        u = UserModel()
        u.email = "smirnov@lawyer.ru"
        u.name = "Алексей Смирнов"
        u.set_password("123")
        u.role = "lawyer"
        u.specialty = "Гражданское право"
        u.experience = "8 лет"
        u.price = "2500 р/час"
        u.schedule = "Пн-Пт 9:00-18:00"
        u.about = (
            "Специализируюсь на гражданских спорах, защите прав потребителей и "
            "договорном праве. Более 8 лет практики в московских судах, "
            "успешно вёл свыше 300 дел."
        )
        db_sess.add(u)

    if not db_sess.query(UserModel).filter(UserModel.email == "vasilyeva@lawyer.ru").first():
        u = UserModel()
        u.email = "vasilyeva@lawyer.ru"
        u.name = "Елена Васильева"
        u.set_password("123")
        u.role = "lawyer"
        u.specialty = "Семейное право"
        u.experience = "5 лет"
        u.price = "2000 р/час"
        u.schedule = "Пн-Сб 10:00-17:00"
        u.about = (
            "Помогаю в вопросах развода, раздела имущества, алиментов и "
            "установления опеки. Бережный и внимательный подход к каждому клиенту."
        )
        db_sess.add(u)

    if not db_sess.query(UserModel).filter(UserModel.email == "petrov@lawyer.ru").first():
        u = UserModel()
        u.email = "petrov@lawyer.ru"
        u.name = "Дмитрий Петров"
        u.set_password("123")
        u.role = "lawyer"
        u.specialty = "Уголовное право"
        u.experience = "12 лет"
        u.price = "3500 р/час"
        u.schedule = "Пн-Пт 10:00-19:00"
        u.about = (
            "Адвокат по уголовным делам с 12-летним стажем. Специализируюсь на "
            "защите в суде первой и апелляционной инстанций, экономических "
            "преступлениях и делах о ДТП."
        )
        db_sess.add(u)

    db_sess.commit()

    s = db_sess.query(SettingsModel).filter(SettingsModel.id == 1).first()
    if not s:
        s = SettingsModel()
        s.id = 1
        s.about_text = (
            'Ю.Р.И.С.Т. — платформа для записи к профессиональным юристам. '
            'Выберите специалиста, удобное время и опишите вашу проблему.'
        )
        s.contact_text = 'Свяжитесь с нами для консультации.'
        db_sess.add(s)
    s.phone = '+7 (985) 541-93-49'
    s.address = 'Детский технопарк Альтаир РТУ МИРЭА'
    db_sess.commit()
