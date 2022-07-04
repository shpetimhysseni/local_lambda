import os
from functools import lru_cache

class Config:
    DB_PATH = f"{os.getenv('LAMBDA_TASK_ROOT')}/app/simple_db.sqlite"


@lru_cache
def get_config():
    return Config()


configuration: Config = get_config()
