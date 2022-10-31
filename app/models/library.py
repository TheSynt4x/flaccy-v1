from app.models import Base
from peewee import CharField, IntegerField, TextField


class Library(Base):
    id = IntegerField(primary_key=True)
    name = CharField()
    path = TextField()
    formats = TextField()
