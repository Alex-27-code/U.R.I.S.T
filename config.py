import os

SECRET_KEY = os.getenv('FLASK_SECRET_KEY', 'urist_dev_secret_key_change_in_production')
UPLOAD_FOLDER = os.path.join('static', 'uploads')
DATABASE_PATH = os.getenv('DATABASE_PATH', 'data/urist.db')
HOST = os.getenv('FLASK_HOST', '0.0.0.0')
PORT = int(os.getenv('FLASK_PORT', 5555))
MAIL_USER = os.getenv('MAIL_USER', 'alex2707berezin@yandex.ru')
MAIL_PASS = os.getenv('MAIL_PASS', 'Aeb2424321!')
MAIL_TO = 'aeb27079@gmail.com'
