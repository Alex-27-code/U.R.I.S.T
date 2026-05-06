import os
import sys
import logging

_project_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(_project_dir)
sys.path.insert(0, _project_dir)

from config import DATABASE_PATH, HOST, PORT
from backend.database import global_init
import backend.database.default_data as dd
from app import app

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

if __name__ == '__main__':
    global_init(DATABASE_PATH)
    dd.default_data()
    logger.info('Starting U.R.I.S.T application')
    app.run(port=PORT, host=HOST, debug=False)
