import asyncio
from concurrent.futures.thread import ThreadPoolExecutor
from functools import partial
from typing import List, Optional

from pydub import AudioSegment

from app import libs, models, schemas
from app.core import logger, settings


from peewee import DoesNotExist

from pathlib import Path


class AudioService:
    def export_audio(self, output_path: str, song_path: str):
        song, flac = libs.song.get_song_info(song_path)

        album_directory = libs.file.get_album_directory(output_path, song)

        song.source_file = song_path
        song.output_file = libs.file.get_export_filename(album_directory, song)

        try:
            db_song = models.Song.get_by_output_file(song.output_file)
        except DoesNotExist:
            db_song = None

        if libs.file.export_exists(album_directory, song) and db_song:
            if not db_song.is_processed:
                db_song.is_processed = True
                db_song.save()
                return

            if db_song.is_uploaded:
                return

        audio = AudioSegment.from_file(song.source_file)
        audio.export(song.output_file, format="mp3", bitrate="320K")

        if song.cover:
            libs.file.save_image(album_directory, song)

        mp3_outfile = libs.tag.tag(flac, song)

        first_album_image = libs.file.get_first_image(song.source_file)
        if first_album_image:
            libs.file.copy_cover(album_directory, first_album_image)

            if not mp3_outfile.get("APIC", None):
                with open(first_album_image.absolute(), "rb") as data:
                    libs.tag.set_apic(mp3_outfile, data.read())

        if not (song.cover and first_album_image):
            cover = libs.discogs.get_album_art(song)

            if cover:
                libs.file.save_image_from_url(album_directory, cover)

                with open(f"{album_directory}\\cover.jpeg", "rb") as data:
                    libs.tag.set_apic(mp3_outfile, data.read())

        libs.song.process_song(song, is_processed=1)

        models.UploadedAlbum.get_or_create(
            **{
                "name": song.album,
                "artist": song.artist,
                "source_path": libs.file.get_parent_path(song.source_file),
                "output_path": libs.file.get_parent_path(song.output_file),
                "is_uploaded": 0,
            }
        )

        logger.info(f"{song.title} export successful")

    async def process_songs(
        self,
        library: schemas.Library,
        songs: List[str] = None,
        output_path: Optional[str] = None,
        source_path: Optional[str] = None,
    ):
        if not songs:
            songs = []

        loop = asyncio.get_running_loop()
        executor = ThreadPoolExecutor(max_workers=4)
        futures = []

        if output_path:
            library.output_path = output_path

        if source_path:
            library.path = source_path

        for song in songs:
            futures.append(
                loop.run_in_executor(
                    executor, partial(self.export_audio, library.output_path, song)
                )
            )

        await asyncio.gather(*futures)


audio = AudioService()
