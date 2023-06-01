import asyncio
from operator import attrgetter
from typing import List, Optional

from fastapi import FastAPI, Query, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware

from app import libs, models, schemas, services
from app.core import logger, settings
from app.db import db

db.create_tables([models.Library, models.Song, models.Album])

app = FastAPI()

origins = [
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/libraries", response_model=schemas.Libraries)
def get_libraries(
    page: Optional[int] = 1,
    per_page: Optional[int] = 10,
    name: Optional[str] = None,
    formats: List[str] = Query(None, description="List of formats"),
    sorts: List[str] = Query(None, description="List of sort params"),
):
    query = models.Library.select()

    if name:
        query = query.where(models.Library.name.contains(name))

    if formats:
        query = query.where(models.Library.formats.contains(",".join(formats)))

    if sorts:
        for sort in sorts:
            key, order = sort.split(".")

            if order == "asc":
                query = query.order_by(attrgetter(key)(models.Song).asc())
            elif order == "desc":
                query = query.order_by(attrgetter(key)(models.Song).desc())

    total_count = query.count()
    if per_page <= 0:
        per_page = total_count

    query = query.paginate(page, per_page)

    return {"libraries": [q for q in query], "total_count": total_count}


@app.get("/api/songs", response_model=schemas.Songs)
def get_songs(
    page: Optional[int] = 1,
    per_page: Optional[int] = 10,
    q: Optional[str] = None,
    sorts: List[str] = Query(None, description="List of sort params"),
):
    query = models.Song.select()

    if q:
        query = query.where(
            models.Song.title.contains(q)
            | models.Song.artist.contains(q)
            | models.Song.album.contains(q)
            | models.Song.year.contains(q)
        )

    if sorts:
        for sort in sorts:
            key, order = sort.split(".")

            if order == "asc":
                query = query.order_by(attrgetter(key)(models.Song).asc())
            elif order == "desc":
                query = query.order_by(attrgetter(key)(models.Song).desc())

    total_count = query.count()
    if per_page <= 0:
        per_page = total_count

    query = query.paginate(page, per_page)

    return {"songs": [q for q in query], "total_count": total_count}


@app.get("/api/songs/total")
def get_songs_total():
    return {"total": models.Song.select().count()}


@app.get("/api/songs/artists/total")
def get_songs_artists_total():
    return {"total": models.Song.select(models.Song.artist).distinct().count()}


@app.get("/api/songs/albums/total")
def get_songs_albums_total():
    return {"total": models.Song.select(models.Song.album).distinct().count()}


@app.get("/api/libraries/total")
def get_libraries_total():
    return {"total": models.Library.select().count()}


async def ws_send(obj_to_send: dict, websocket: WebSocket):
    logger.info(obj_to_send)
    await websocket.send_json(obj_to_send)


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()

    try:
        while True:
            data = await websocket.receive_json()

            command = data.get("command")
            params = data.get("params", [])

            logger.info(f"Received command: {command} with params: {params}")

            if command == "sync":
                settings.disable_ftp = True

                libraries = [
                    schemas.Library(**library) for library in models.Library.all()
                ]
                processed_songs = [
                    p.source_file for p in models.Song.get_processed_songs()
                ]

                for library in libraries:
                    songs = list(
                        set(libs.file.get_song_files(library)) - set(processed_songs)
                    )

                    services.audio.process_songs(library, songs)

                if not settings.disable_ftp:
                    services.audio.upload_albums(models.Album.get_unuploaded_albums())

                await ws_send(
                    {"command": "sync", "status": "start_refreshing_songs"}, websocket
                )

                await asyncio.sleep(10)

                await ws_send({"command": "sync", "status": "success"}, websocket)
    except WebSocketDisconnect:
        pass
