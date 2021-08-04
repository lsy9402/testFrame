import os
from enum import Enum
from json import loads
from pathlib import Path
from string import octdigits
from typing import Type, Any

from pydantic import BaseSettings, validator, Field
from yaml import full_load

from utils.IPUtil import get_host_ip


def _missing_(cls, value):
    for item in cls:
        if item.value.upper() == value.upper():
            return item


database_driven = {
    "mysql": "pymysql"
}


class Settings(BaseSettings):
    ENV: Type[Enum]

    @validator("ENV", pre=True)
    def gun_env(cls, value):
        _ENV = Enum("ENV", {_env: _env for _env in loads(value)})
        _ENV._missing_ = classmethod(_missing_)
        return _ENV

    LOG_DIR: Path
    LOG_LEVEL: Enum("LEVEL", {level: level for level in ("TRACE", "DEBUG", "INFO", "SUCCESS", "WARNING", "ERROR", "CRITICAL")})

    @validator("LOG_DIR", pre=True)
    def gun_log_dir(cls, value):
        log_dir = Path(value)
        log_dir.mkdir(parents=True, exist_ok=True)
        return log_dir

    SQL: Any

    @validator("SQL", pre=True)
    def load_sql(cls, value):
        with Path(value).open() as f:
            return full_load(f)

    # database_driven
    DB_TYPE: Enum("DB_TYPE", {db: db for db in database_driven})
    DB_USER: str
    DB_CRYPT: str
    DB_CRYPT_KEY: str = octdigits
    DB_PASSWORD: str

    @validator("DB_PASSWORD")
    def crypt_db_password(cls, value, values):
        if values.get("DB_CRYPT").upper() == "DES":
            from utils.EncryptUtil import des_crypt

            return des_crypt(value, key=values.get("DB_CRYPT_KEY"))

    DB_HOST: str
    DB_PORT: int
    DB_NAME: str

    LOCALHOST: str = Field(default_factory=get_host_ip)

    class Config:
        env_file = os.environ.get("ENV_FILE", ".env")
        use_enum_values = True


settings = Settings()
