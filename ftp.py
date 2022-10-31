import os
import os.path
from ftplib import FTP, error_perm
from pathlib import Path

from utils.to_async import async_wrap

try:
    ftp = FTP()
    ftp.connect("192.168.0.221", 2100)
    ftp.login("anonymous", "l")
except Exception as e:
    print(e)

    ftp = None


def place_files(path):
    if ftp is None:
        print("Need to start foobar2000 ftp server")
        return

    ftp.cwd("/foobar2000 Music Folder")

    p = Path(path)

    if os.path.isdir(path):
        try:
            ftp.mkd(p.name)

        except error_perm as e:
            if not e.args[0].startswith("550"):
                raise

        print("CWD", path.name)
        ftp.cwd(path.name)

        for root, _, files in os.walk(path):
            for f in files:
                ftp.storbinary("STOR " + f, open(os.path.join(root, f), "rb"))
