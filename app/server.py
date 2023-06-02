from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app import api, models
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

app.include_router(api.songs_router, tags=["songs"])
app.include_router(api.artists_router, tags=["artists"])
app.include_router(api.stats_router, tags=["stats"])
app.include_router(api.ws_commands_router, tags=["websockets"])
app.include_router(api.libraries_router, tags=["libraries"])
