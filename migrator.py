import asyncio
from functools import partial

from app import libs, models, schemas
from app.core import logger
from configurator import create_tables

from concurrent.futures.thread import ThreadPoolExecutor

create_tables()


def export_audio(output_path: str, song_path: str):
    song, _ = libs.song.get_song_info(song_path)

    # logger.info(_)

    # return

    album_directory = libs.file.get_album_directory(output_path, song)

    song.source_file = song_path
    song.output_file = libs.file.get_export_filename(album_directory, song)

    libs.song.process_song(song, 1, 1)

    logger.info(f"Processed {song.title}")


# export_audio(
#     "D:\Music\Output",
#     "D:\\Music\\FLAC\\complete\\ABARE_ABARE_ABARE\\Midori - album 2010.05.19 - Shinsekai [FLAC]\\02 ミドリ - 凡庸VS茫洋.flac",
# )


async def migrator():
    loop = asyncio.get_running_loop()
    executor = ThreadPoolExecutor(max_workers=2)

    futures = []

    libraries = [schemas.Library(**l) for l in models.Library.select().dicts()]

    for library in libraries:
        for song_path in libs.file.get_song_files(library):
            futures.append(
                loop.run_in_executor(
                    executor,
                    partial(export_audio, library.output_path, song_path),
                )
            )

    await asyncio.gather(*futures)


if __name__ == "__main__":
    asyncio.run(migrator())
