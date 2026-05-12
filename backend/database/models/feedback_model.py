import sqlalchemy
from datetime import datetime
from backend.database.db_session import SqlAlchemyBase


class FeedbackModel(SqlAlchemyBase):
    __tablename__ = 'feedback'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    sender_name = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    sender_email = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    message = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    created_at = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.utcnow)
    is_read = sqlalchemy.Column(sqlalchemy.Boolean, default=False)

    def __repr__(self):
        return f'<Feedback #{self.id} from {self.sender_email}>'
