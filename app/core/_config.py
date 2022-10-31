from typing import List, Optional

from pydantic import BaseSettings


class Config(BaseSettings):
    ftp_server: str = ""
    ftp_username: Optional[str] = None
    ftp_password: Optional[str] = None

    session_albums: List[str] = []

    class Config:
        env_file = ".env"


settings = Config()
