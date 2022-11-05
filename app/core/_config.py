from typing import Optional

from pydantic import BaseSettings


class Config(BaseSettings):
    ftp_server: str = ""
    ftp_username: Optional[str] = None
    ftp_password: Optional[str] = None

    discogs_token: Optional[str] = None

    disable_ftp: bool = False
    override_source_path: Optional[str] = None
    override_output_path: Optional[str] = None
    force: bool = False

    class Config:
        env_file = ".env"


settings = Config()
