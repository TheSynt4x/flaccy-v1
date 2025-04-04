import os
from asyncio.log import logger
from ftplib import FTP, error_perm
from pathlib import Path

from peewee import DoesNotExist

from app import models
from app.core import settings
from app.utils import clean_filename


class FtpWrapper:
    def __init__(self):
        server, port = settings.ftp_server.split(":")

        self.server = server
        self.port = int(port)

        self.success = []
        self.failed = []

    def connect(self):
        self.ftp = FTP()

        self.ftp.encoding = "utf-8"

        try:
            self.ftp.connect(self.server, self.port)
            self.ftp.login(settings.ftp_username, settings.ftp_password)

            self.ftp.sendcmd("OPTS UTF8 ON")
        except Exception as e:
            logger.error(e)
            self.ftp = None

    def upload_files(self, path: str):
        if not self.ftp:
            logger.info("You need to start your FTP server")
            return

        self.ftp.cwd("/foobar2000 Music Folder")

        p = Path(path)

        if os.path.isdir(path):
            try:
                self.ftp.mkd(p.name)
            except error_perm as e:
                if not e.args[0].startswith("550"):
                    raise

            logger.info(f"Uploading {p.name}")

            self.ftp.cwd(p.name)

            for root, _, files in os.walk(path):
                for f in files:
                    full_path = os.path.join(root, f)
                    fp = Path(full_path)

                    self.ftp.storbinary(
                        "STOR " + clean_filename(f).strip(), open(full_path, "rb")
                    )

                    if fp.suffix in [".mp3"]:
                        try:
                            models.Song.update_upload_status(full_path, True)
                        except DoesNotExist as e:
                            logger.info(e)
                            return

            try:
                models.Album.update_upload_status(p, True)
            except DoesNotExist as e:
                logger.info(e)
                return


ftp = FtpWrapper()
