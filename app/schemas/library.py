from pydantic import BaseModel


class Library(BaseModel):
    name: str
    path: str
    output_path: str
    formats: str

    class Config:
        orm_mode: bool = True
