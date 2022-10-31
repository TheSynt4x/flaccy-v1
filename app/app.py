import asyncio
from concurrent.futures.thread import ThreadPoolExecutor
from functools import partial

from app import libs, models, schemas, services
from app.core import settings


async def main():
    loop = asyncio.get_running_loop()
    executor = ThreadPoolExecutor(max_workers=4)
    futures = []

    libraries = [schemas.Library(**l) for l in models.Library.select().dicts()]

    for library in libraries:
        processed_songs = [
            p.source_file
            for p in models.Song.select().where(models.Song.is_processed == 1)
        ]

        difference = list(set(libs.file.get_song_files(library)) - set(processed_songs))

        for song in difference:
            futures.append(
                loop.run_in_executor(
                    executor,
                    partial(services.audio.export_audio, library.output_path, song),
                )
            )

    await asyncio.gather(*futures)

    for album in settings.session_albums:
        services.ftp.upload_files(album)
