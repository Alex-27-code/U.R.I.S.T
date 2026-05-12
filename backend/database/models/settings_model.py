import sqlalchemy
from backend.database.db_session import SqlAlchemyBase


class SettingsModel(SqlAlchemyBase):
    __tablename__ = 'settings'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    about_text = sqlalchemy.Column(
        sqlalchemy.String,
        nullable=False,
        default='Мы предоставляем профессиональные юридические услуги.',
    )
    contact_text = sqlalchemy.Column(
        sqlalchemy.String,
        nullable=False,
        default='Контакты',
    )
    phone = sqlalchemy.Column(
        sqlalchemy.String,
        nullable=False,
        default='+7 (999) 123-45-67',
    )
    address = sqlalchemy.Column(
        sqlalchemy.String,
        nullable=False,
        default='Москва, ул. Примерная, д.1',
    )

    def __repr__(self):
        return f'<Settings #{self.id}>'
