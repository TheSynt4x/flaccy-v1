from typing import Any, Dict, List, Optional

from pydantic import BaseSettings


class Config(BaseSettings):
    output_path: str = "C:/Music"

    class Config:
        env_file = ".env"


settings = Config()
