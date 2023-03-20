from typing import List, Optional

from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware

from app import models
from app.core import logger
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


@app.get("/api/libraries")
def get_libraries(
    page: Optional[int] = 1,
    name: Optional[str] = None,
    formats: List[str] = Query(None, description="List of formats"),
):
    query = models.Library.select()

    if name:
        query = query.where(models.Library.name.contains(name))

    if formats:
        query = query.where(models.Library.formats.contains(",".join(formats)))

    query = query.paginate(page, 10)

    return {"libraries": [q for q in query]}


@app.get("/api/songs")
def get_songs(
    page: int = 1,
    name: Optional[str] = None,
    artist: Optional[str] = None,
    album: Optional[str] = None,
    year: Optional[int] = None,
    is_processed: Optional[bool] = None,
):
    query = models.Song.select()

    if name:
        query = query.where(models.Song.name.contains(name))

    if artist:
        query = query.where(models.Song.artist.contains(artist))

    if album:
        query = query.where(models.Song.album.contains(album))

    if year:
        query = query.where(models.Song.year == year)

    if is_processed is not None:
        query = query.where(models.Song.is_processed == is_processed)

    query = query.paginate(page, 10)

    return {"songs": [q for q in query]}


@app.websocket("/ws")
async def websocket_endpoint(websocket):
    await websocket.accept()
    while True:
        data = await websocket.recieve_json()

        command = data.get("command")
        params = data.get("params", [])

        logger.info(f"Received command: {command} with params: {params}")

        if command == "scan":
            await websocket.send_json({"status": "scanning"})

            # TODO: scan library

            await websocket.send_json({"status": "done"})
