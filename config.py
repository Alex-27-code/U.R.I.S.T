"""
Конфигурация приложения U.R.I.S.T.
Все настройки собраны в одном месте для удобства управления.
"""
import os

# Секретный ключ для Flask-сессий и CSRF-защиты.
# В production ОБЯЗАТЕЛЬНО задать через переменную окружения FLASK_SECRET_KEY.
SECRET_KEY = os.getenv('FLASK_SECRET_KEY', 'urist_dev_secret_key_change_in_production')

# Путь к папке для загруженных файлов (фото профиля)
UPLOAD_FOLDER = os.path.join('static', 'uploads')

# Путь к файлу базы данных SQLite
DATABASE_PATH = os.getenv('DATABASE_PATH', 'data/urist.db')

# Настройки сервера
HOST = os.getenv('FLASK_HOST', '0.0.0.0')
PORT = int(os.getenv('FLASK_PORT', 5555))

# Настройки почты для обратной связи
MAIL_USER = os.getenv('MAIL_USER', '')   # Яндекс-адрес отправителя, например mybot@yandex.ru
MAIL_PASS = os.getenv('MAIL_PASS', '')   # Пароль от Яндекс почты (или пароль приложения)
MAIL_TO = 'aeb27079@gmail.com'           # Куда приходят письма обратной связи
