from typing import List, Optional

from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware

from app import models, schemas
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


@app.get("/api/libraries", response_model=schemas.Libraries)
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

    total_count = query.count()
    query = query.paginate(page, 10)

    return {"libraries": [q for q in query], "total_count": total_count}


@app.get("/api/songs", response_model=schemas.Songs)
def get_songs(
    page: int = 1,
    q: Optional[str] = None,
    sort: List[str] = [],
    artist: Optional[str] = None,
    album: Optional[str] = None,
    year: Optional[int] = None,
    is_processed: Optional[bool] = None,
):
    query = models.Song.select()

    if q:
        query = query.where(
            models.Song.title.contains(q)
            | models.Song.artist.contains(q)
            | models.Song.album.contains(q)
            | models.Song.year.contains(q)
        )

    if artist:
        query = query.where(models.Song.artist.contains(artist))

    if album:
        query = query.where(models.Song.album.contains(album))

    if year:
        query = query.where(models.Song.year == year)

    if is_processed is not None:
        query = query.where(models.Song.is_processed == is_processed)

    if sort:
        for sort in sort:
            key, order = sort.split(".")

            if order == "asc":
                query = query.order_by(models.Song[key].asc())
            elif order == "desc":
                query = query.order_by(models.Song[key].desc())

    total_count = query.count()
    query = query.paginate(page, 10)

    return {"songs": [q for q in query], "total_count": total_count}


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
