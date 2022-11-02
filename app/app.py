import asyncio
from typing import Optional

import typer

from app import libs, models, schemas, services
from app.core import logger
from app.db import db

app = typer.Typer()


@app.command()
def setup():
    """
    Setup the program, add libraries, output paths, etc
    """

    db.create_tables([models.Library, models.Song])

    name = typer.prompt("Library name")
    source_path = typer.prompt("Library path")
    output_path = typer.prompt("Output path (where files should be saved)")
    formats = typer.prompt("Library formats (which files are in your library)")

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

    libraries = [schemas.Library(**library) for library in models.Library.all()]

    for library in libraries:
        processed_songs = [p.source_file for p in models.Song.get_processed_songs()]

        songs = list(set(libs.file.get_song_files(library)) - set(processed_songs))

        typer.echo(
            asyncio.run(
                services.audio.process_songs(
                    library,
                    songs,
                    output_path,
                    source_path,
                    disable_ftp,
                )
            )
        )


@app.command()
def full_sync(
    output_path: Optional[str] = None,
    source_path: Optional[str] = None,
    disable_ftp: bool = False,
):
    """
    Run a full sync for all saved libraries.
    """

    confirm = typer.confirm("Are you sure you want to run a full sync?")

    if not confirm:
        logger.info("Not running a full sync")
        raise typer.Abort()

    libraries = [schemas.Library(**library) for library in models.Library.all()]

    for library in libraries:
        songs = libs.file.get_song_files(library)

        typer.echo(
            asyncio.run(
                services.audio.process_songs(
                    library,
                    songs,
                    output_path,
                    source_path,
                    disable_ftp,
                )
            )
        )
