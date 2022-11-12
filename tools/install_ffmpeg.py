import os
import sys
import time
import zipfile

import requests

to_download = (
    "https://github.com/BtbN/FFmpeg-Builds/releases/download/"
    "latest/ffmpeg-master-latest-win64-gpl.zip"
)

if os.path.exists("C:\\ffmpeg.zip"):
    print("Cleaning up...\n")
    os.remove("C:\\ffmpeg.zip")

if os.path.exists("C:\\ffmpeg"):
    raise Exception("ffmpeg already installed")


with requests.get(to_download, stream=True) as r:
    with open("C:\\ffmpeg.zip", "wb") as file:
        total_size = int(r.headers.get("Content-Length"))
        chunk_size = 1024 * 1024
        for i, chunk in enumerate(r.iter_content(chunk_size=chunk_size)):
            if not chunk:
                break

            file.write(chunk)

            c = i * chunk_size / total_size * 100

            sys.stdout.write(f"\rDownloading ffmpeg {round(c, 4)}%")
            time.sleep(0.1)
            sys.stdout.flush()

zip = zipfile.ZipFile("C:\\ffmpeg.zip")
zip.extractall("C:\\")

os.rename("C:\\ffmpeg-master-latest-win64-gpl", "C:\\ffmpeg")

print("\nAdding ffmpeg to PATH\n")
os.system('setx /m PATH "C:\\ffmpeg\\bin;%PATH%"')

print("You may now run Flaccy\n")
