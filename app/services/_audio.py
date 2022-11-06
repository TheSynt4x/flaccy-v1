from concurrent.futures import as_completed
from concurrent.futures.thread import ThreadPoolExecutor
from typing import List

from peewee import DoesNotExist
from pydub import AudioSegment

from app import libs, models, schemas
from app.core import logger, settings


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

        if (
            libs.file.export_exists(album_directory, song)
            and db_song
            and not settings.force
        ):
            if db_song.is_processed and db_song.is_uploaded:
                return

            if not db_song.is_processed:
                db_song.is_processed = True
                db_song.save()
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

        if not (
            song.cover
            or first_album_image
            and libs.file.get_first_image(song.output_file)
        ):
            cover = libs.discogs.get_album_art(song)

            if cover:
                libs.file.save_image_from_url(album_directory, cover)

                with open(f"{album_directory}\\cover.jpg", "rb") as data:
                    libs.tag.set_apic(mp3_outfile, data.read())

        libs.song.process_song(song, is_processed=1)

        try:
            album = models.Album.get_by_output_path(
                libs.file.get_parent_path(song.output_file)
            )

            album.is_uploaded = 0
            album.save()
        except DoesNotExist:
            models.Album.create(
                name=song.album,
                artist=song.artist,
                year=song.year,
                source_path=libs.file.get_parent_path(song.source_file),
                output_path=libs.file.get_parent_path(song.output_file),
                is_uploaded=0,
            )

        logger.info(f"{song.title} export successful")

    def process_songs(self, library: schemas.Library, songs: List[str] = None):
        if not songs:
            songs = []

        with ThreadPoolExecutor(max_workers=4) as executor:
            futures = []

            for song in songs:
                futures.append(
                    executor.submit(self.export_audio, library.output_path, song)
                )

            for future in as_completed(futures):
                future.result()

    def upload_albums(self, albums):
        libs.ftp.connect()

        for album in albums:
            libs.ftp.upload_files(album.output_path)


audio = AudioService()
