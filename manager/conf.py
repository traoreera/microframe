import os

from configurations import manager
from dotenv import find_dotenv, load_dotenv

cfg = manager.ManagerCfg(manager.Configure())


load_dotenv(
    dotenv_path=find_dotenv(filename=cfg.custom_config["dotenv"], raise_error_if_not_found=True)
)


class Database:
    URL: str = os.getenv("DATA_URL")
