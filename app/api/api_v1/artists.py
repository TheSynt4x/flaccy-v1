from fastapi import APIRouter

from app import libs

router = APIRouter()


@router.get("/api/artists/{artist_name}")
def get_artist(artist_name: str):
    """
    Get artist by name
    """
    return libs.discogs.get_artist_information(artist_name)
