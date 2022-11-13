import os

from app.app import app

if os.path.exists("C:\\ffmpeg.zip"):
    os.remove("C:\\ffmpeg.zip")

if not os.path.exists("C:\\ffmpeg"):
    try:
        from tools import install_ffmpeg  # noqa
    except Exception:
        pass

if __name__ == "__main__":
    app()
