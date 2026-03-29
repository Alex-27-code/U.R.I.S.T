import datetime
import sqlalchemy
from sqlalchemy import orm
from backend.database.db_session import SqlAlchemyBase

class BookingModel(SqlAlchemyBase):
    __tablename__ = 'bookings'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    client_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('users.id'))
    lawyer_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('users.id'))
    
    date = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    time = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    problem = sqlalchemy.Column(sqlalchemy.Text, nullable=False)
    
    created_date = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.now)

    client = orm.relationship('UserModel', foreign_keys=[client_id], backref='my_bookings')
    lawyer = orm.relationship('UserModel', foreign_keys=[lawyer_id], backref='lawyer_bookings')
