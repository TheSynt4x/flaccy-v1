from peewee import CharField, IntegerField, TextField

from app.models import Base


class Library(Base):
    id = IntegerField(primary_key=True)
    name = CharField()
    path = TextField()
    output_path = CharField()
    formats = TextField()

    @classmethod
    def all(cls: "Library") -> "Library":
        return [l for l in cls.select().dicts()]