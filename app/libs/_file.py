import glob
import os
import shutil
from pathlib import Path
from typing import List

import requests

from app import schemas
from app.utils import clean_filename


class FileWrapper:
    def get_song_files(self, library: schemas.Library) -> List[str]:
        files = []

        for filename in glob.iglob(f"{library.path}/**/*", recursive=True):
            ending = Path(filename).suffix
            if ending in library.formats.split(","):
                files.append(filename)

        return files

    def get_first_image(self, song_path: str):
        p = Path(song_path).parent.absolute()

        for root, _, files in os.walk(p):
            for f in files:
                cover_file = os.path.join(root, f)

                file_path = Path(cover_file)

                if file_path.name.lower() in ["cover.jpg", "cover.png", "cover.jpeg"]:
                    return file_path

                if file_path.suffix in [".jpg", ".png", ".jpeg"]:
                    return file_path

        return None

    def get_album_directory(self, output_path, song: schemas.Song):
        album_directory = os.path.join(
            output_path, clean_filename(f"{song.artist} - {song.album}")
        )

        if song.year and "Z" not in song.year:
            album_directory += f" ({song.year})"

        Path(album_directory).mkdir(parents=True, exist_ok=True)

        return album_directory

    def get_parent_path(self, path: str):
        return Path(path).parent.absolute()

    def save_image(self, album_directory: str, song: schemas.Song):
        with open(f"{album_directory}\\cover.png", "wb") as binary_file:
            binary_file.write(song.cover)

    def save_image_from_url(self, album_directory: str, image_url: str):
        response = requests.get(
            image_url,
            headers={
                "user-agent": (
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/106.0.0.0 Safari/537.36"
                )
            },
        )

        if not response.ok:
            return

        with open(f"{album_directory}\\cover.jpg", "wb") as f:
            f.write(response.content)

    def get_export_filename(self, album_directory: str, song: schemas.Song):
        return os.path.join(album_directory, clean_filename(f"{song.title}.mp3"))

    def export_exists(self, album_directory: str, song: schemas.Song):
        return os.path.exists(self.get_export_filename(album_directory, song))

    def copy_cover(self, album_directory: str, first_album_image: Path):
        shutil.copy(
            first_album_image.absolute(),
            os.path.join(album_directory, f"cover{first_album_image.suffix}"),
        )


file = FileWrapper()
