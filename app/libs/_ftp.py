import os
from asyncio.log import logger
from ftplib import FTP, error_perm
from pathlib import Path

from app import models
from app.core import settings


class FtpWrapper:
    def __init__(self):
        server, port = settings.ftp_server.split(":")
        self.ftp = FTP()

        try:
            self.ftp.connect(server, int(port))
            self.ftp.login(settings.ftp_username, settings.ftp_password)
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

                    self.ftp.storbinary("STOR " + f, open(full_path, "rb"))

                    if fp.suffix not in [".jpg", ".png", ".jpeg"]:
                        models.Song.update_upload_status(full_path, True)


ftp = FtpWrapper()
