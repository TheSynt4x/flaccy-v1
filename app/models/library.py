from peewee import CharField, IntegerField, TextField

from app.models.base import Base


class Library(Base):
    id = IntegerField(primary_key=True)
    name = CharField()
    path = TextField()
    output_path = CharField()
    formats = TextField()

    @classmethod
    def all(cls: "Library") -> "Library":
        return [library for library in cls.select().dicts()]
