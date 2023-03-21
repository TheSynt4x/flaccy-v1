from typing import List

from pydantic import BaseModel


class BaseLibrary(BaseModel):
    name: str
    path: str
    output_path: str
    formats: str

    class Config:
        orm_mode: bool = True


class Library(BaseLibrary):
    id: int


class Libraries(BaseModel):
    libraries: List[Library] = []
    total_count: int = 0
