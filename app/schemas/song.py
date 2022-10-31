from typing import Any, Optional

from pydantic import BaseModel


class Song(BaseModel):
    title: Optional[str] = None
    artist: Optional[str] = None
    album: Optional[str] = None
    year: Optional[str] = None
    cover: Optional[Any] = None
    source_file: Optional[str] = None
    output_file: Optional[str] = None

    class Config:
        orm_mode: bool = True
