import asyncio
import shutil
from functools import partial, wraps
from os import path, walk
from os.path import exists
from pathlib import Path

from mutagen.easyid3 import EasyID3
from mutagen.flac import FLAC
from mutagen.id3 import APIC, ID3
from pydub import AudioSegment

from ftp import place_files
from utils.files import clean_filename
from utils.songs import get_song_files
from utils.to_async import async_wrap

libraries = [
    {
        "source": "D:\Music\FLAC\complete",
        "formats": [".flac"],
    }
]

SESSION_SONGS = []


class Song:
    def __init__(self, path, song_name, artist, album, year, art=None, flac=None):
        self.path = path
        self.name = song_name
        self.artist = artist
        self.album = album
        self.year = year
        self.cover = art

        self.flac = flac


output_path = "D:\Music\Output"


def get_song_field(flac, name):
    return flac.get(name)[0] if len(flac.get(name, [])) else None


def get_song_info(song_path: str):
    flac = FLAC(song_path)

    song_name = get_song_field(flac, "title")
    artist = get_song_field(flac, "artist") or get_song_field(flac, "albumartist")
    album = get_song_field(flac, "album")
    year = get_song_field(flac, "originalyear") or get_song_field(flac, "date")

    art = None
    if len(flac.pictures):
        art = flac.pictures[0].data

    return Song(
        song_path,
        song_name,
        artist,
        album,
        year,
        art,
        flac=flac,
    )


def tagify(song: Song, outfile: str):
    mp3 = EasyID3(outfile)

    for tag in song.flac.keys():
        if tag in list(mp3.valid_keys.keys()):
            mp3[tag] = song.flac[tag]

    mp3.save()

    mp3_pic = ID3(outfile)  # in case we want to add a pic

    if song.cover:
        mp3_pic["APIC"] = APIC(
            encoding=0, mime="image/png", type=3, desc="Cover", data=song.cover
        )

        mp3_pic.save()

    return mp3_pic


def get_first_image(song_path):
    p = Path(song_path).parent.absolute()

    for root, _, files in walk(p):
        for f in files:
            cover_file = path.join(root, f)

            file_path = Path(cover_file)

            if file_path.name.lower() in ["cover.jpg", "cover.png"]:
                return file_path

            if file_path.suffix in [".jpg", ".png"]:
                return file_path

    return None


@async_wrap
def export_audio(song_path: str):
    song = get_song_info(song_path)

    album_directory = path.join(
        output_path, clean_filename(f"{song.artist} - {song.album}")
    )

    if song.year:
        album_directory += f" ({song.year})"

    outfile = path.join(album_directory, clean_filename(f"{song.name}.mp3"))

    if exists(outfile):
        with open("logs/processed.log", "a+", encoding="utf-8") as processed:
            processed.write(f"{song_path}\n")

        return

    Path(album_directory).mkdir(parents=True, exist_ok=True)

    audio = AudioSegment.from_file(song.path)
    audio.export(outfile, format="mp3", bitrate="320K")

    if song.cover:
        with open(f"{album_directory}\\cover.jpg", "wb") as binary_file:
            binary_file.write(song.cover)

    mp3_audio = tagify(song, outfile)

    first_album_image = get_first_image(song_path)

    if first_album_image:
        shutil.copy(
            first_album_image.absolute(),
            path.join(album_directory, first_album_image.name),
        )

        with open(first_album_image.absolute(), "rb") as data:
            mp3_audio["APIC"] = APIC(
                encoding=0, mime="image/png", type=3, desc="Cover", data=data.read()
            )

            mp3_audio.save()

    print(f"{outfile} done")

    with open("logs/processed.log", "a+", encoding="utf-8") as processed:
        processed.write(f"{song_path}\n")

    p = Path(outfile).parent.absolute()
    if p not in SESSION_SONGS:
        SESSION_SONGS.append(p)


async def main():
    songs = []
    other = []

    processed_songs = []
    with open("logs/processed.log", "r", encoding="utf-8") as f:
        text = f.read()

        for song in text.splitlines():
            processed_songs.append(song)

    flac_songs = get_song_files(libraries[0])

    difference = list(set(flac_songs) - set(processed_songs))

    print(difference)

    for flac_song in difference:
        songs.append(export_audio(flac_song))

    await asyncio.gather(*songs)

    for s in SESSION_SONGS:
        other.append(place_files(s))

    await asyncio.gather(*other)


asyncio.run(main())
