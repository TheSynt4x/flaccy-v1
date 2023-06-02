from fastapi import APIRouter

from app import models

router = APIRouter()


@router.get("/api/songs/total")
def get_songs_total():
    return {"total": models.Song.select().count()}


@router.get("/api/songs/artists/total")
def get_songs_artists_total():
    return {"total": models.Song.select(models.Song.artist).distinct().count()}


@router.get("/api/songs/albums/total")
def get_songs_albums_total():
    return {"total": models.Song.select(models.Song.album).distinct().count()}


@router.get("/api/libraries/total")
def get_libraries_total():
    return {"total": models.Library.select().count()}
