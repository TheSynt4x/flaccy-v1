from operator import attrgetter
from typing import List, Optional

from fastapi import APIRouter, Query

from app import models, schemas

router = APIRouter()


@router.get("/api/libraries", response_model=schemas.Libraries)
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
