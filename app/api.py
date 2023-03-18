from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app import models
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
def get_libraries():
    return {"libraries": models.Library.all()}
