import asyncio
from typing import Optional

import typer
from rich.prompt import Confirm, Prompt

from app import libs, models, schemas, services
from app.core import logger, settings
from app.db import db

db.create_tables([models.Library, models.Song, models.Album])

app = typer.Typer()


@app.command()
def setup():
    """
    Setup the program, add libraries, output paths, etc
    """

    name = Prompt.ask("Library name")
    source_path = Prompt.ask("Library path")
    output_path = Prompt.ask("Output path (where files should be saved)")
    formats = Prompt.ask("Library formats (which files are in your library)")

    library = models.Library(
        name=name, path=source_path, output_path=output_path, formats=formats
    )

    library.save()

    typer.echo("You may now run a full sync!")


@app.command()
def sync(
    output_path: Optional[str] = None,
    source_path: Optional[str] = None,
    disable_ftp: bool = False,
):
    """
    Run a normal sync for all saved libraries.
    """

    settings.override_source_path = source_path
    settings.override_output_path = output_path
    settings.disable_ftp = disable_ftp

    if not settings.disable_ftp:
        libs.ftp.connect()

    libraries = [schemas.Library(**library) for library in models.Library.all()]
    processed_songs = [p.source_file for p in models.Song.get_processed_songs()]

    for library in libraries:
        songs = list(set(libs.file.get_song_files(library)) - set(processed_songs))

        asyncio.run(services.audio.process_songs(library, songs))

    if not settings.disable_ftp:
        for album in models.Album.get_unuploaded_albums():
            libs.ftp.upload_files(album.output_path)


@app.command()
def full_sync(
    output_path: Optional[str] = None,
    source_path: Optional[str] = None,
    disable_ftp: bool = False,
):
    """
    Run a full sync for all saved libraries.
    """

    settings.override_source_path = source_path
    settings.override_output_path = output_path
    settings.disable_ftp = disable_ftp

    if not settings.disable_ftp:
        libs.ftp.connect()

    confirm = Confirm.ask("Are you sure you want to run a full sync?")

    if not confirm:
        logger.info("Not running a full sync")
        raise typer.Abort()

    libraries = [schemas.Library(**library) for library in models.Library.all()]

    for library in libraries:
        songs = libs.file.get_song_files(library)

        asyncio.run(services.audio.process_songs(library, songs))

    if not settings.disable_ftp:
        for album in models.Album.get_unuploaded_albums():
            libs.ftp.upload_files(album.output_path)


@app.command()
def db_diff(
    output_path: Optional[str] = None,
    source_path: Optional[str] = None,
    disable_ftp: bool = False,
):
    settings.override_source_path = source_path
    settings.override_output_path = output_path
    settings.disable_ftp = disable_ftp

    libraries = [schemas.Library(**library) for library in models.Library.all()]
    processed_songs = [p.source_file for p in models.Song.get_processed_songs()]

    songs = []

    for library in libraries:
        songs.extend(libs.file.get_song_files(library))

    logger.info(f"songs in output: {len(songs)}, songs in db: {len(processed_songs)}")


@app.command()
def upload_albums():
    libs.ftp.connect()

    for album in models.Album.get_unuploaded_albums():
        libs.ftp.upload_files(album.output_path)
