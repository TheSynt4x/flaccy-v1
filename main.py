import ctypes
import os

from app.app import app

try:
    is_admin = os.getuid() == 0
except AttributeError:
    is_admin = ctypes.windll.shell32.IsUserAnAdmin() != 0

if is_admin:
    if os.path.exists("C:\\ffmpeg.zip"):
        os.remove("C:\\ffmpeg.zip")

    if not os.path.exists("C:\\ffmpeg"):
        try:
            from tools import install_ffmpeg  # noqa
        except Exception as e:
            pass

if __name__ == "__main__":
    app()
