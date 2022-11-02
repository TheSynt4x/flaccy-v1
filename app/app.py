import asyncio
from typing import Optional

import typer

from app import libs, models, schemas, services
from app.core import logger

app = typer.Typer()


@app.command()
def run(output_path: Optional[str] = None, source_path: Optional[str] = None):
    """
    Run a normal sync for all saved libraries.
    """

    libraries = [schemas.Library(**library) for library in models.Library.all()]

    for library in libraries:
        processed_songs = [p.source_file for p in models.Song.get_processed_songs()]

        songs = list(set(libs.file.get_song_files(library)) - set(processed_songs))

        typer.echo(
            asyncio.run(
                services.audio.process_songs(library, songs, output_path, source_path)
            )
        )


@app.command()
def full_sync(output_path: Optional[str] = None, source_path: Optional[str] = None):
    """
    Run a full sync for all saved libraries.
    """

    confirm = typer.confirm("Are you sure you want to run a full sync")

    if not confirm:
        logger.info("Not running a full sync")
        raise typer.Abort()

    libraries = [schemas.Library(**library) for library in models.Library.all()]

    for library in libraries:
        songs = libs.file.get_song_files(library)

        typer.echo(
            asyncio.run(
                services.audio.process_songs(library, songs, output_path, source_path)
            )
        )
