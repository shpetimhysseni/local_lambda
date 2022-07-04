from uszipcode import SearchEngine
from app.configs.config import configuration

se = SearchEngine(db_file_path=configuration.DB_PATH)