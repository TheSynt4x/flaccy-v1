from typing import Any, List, Optional

from pydantic import BaseModel


class BaseSong(BaseModel):
    title: Optional[str] = None
    artist: Optional[str] = None
    album: Optional[str] = None
    year: Optional[str] = None
    cover: Optional[Any] = None
    source_file: Optional[str] = None
    output_file: Optional[str] = None

    class Config:
        orm_mode: bool = True


class Song(BaseSong):
    id: int


class Songs(BaseModel):
    songs: List[Song] = []
    total_count: int = 0
