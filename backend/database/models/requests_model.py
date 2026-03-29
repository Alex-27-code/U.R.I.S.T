import datetime
import sqlalchemy
from sqlalchemy import orm
from backend.database.db_session import SqlAlchemyBase

class ClientRequestModel(SqlAlchemyBase):
    __tablename__ = 'client_requests'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    user_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('users.id'))
    title = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    description = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    created_date = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.now)
    status = sqlalchemy.Column(sqlalchemy.String, default='open')

    user = orm.relationship('UserModel')
