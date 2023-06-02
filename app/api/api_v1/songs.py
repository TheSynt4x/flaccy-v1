from operator import attrgetter
from typing import List, Optional

from fastapi import APIRouter, Query

from app import models, schemas

router = APIRouter()


@router.get("/api/songs", response_model=schemas.Songs)
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
