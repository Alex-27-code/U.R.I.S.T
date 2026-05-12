import os
import sys

_project_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(_project_dir)
sys.path.insert(0, _project_dir)

from config import DATABASE_PATH
from backend.database import global_init
import backend.database.default_data as dd

global_init(DATABASE_PATH)
dd.default_data()

from app import app
