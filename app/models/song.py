from app.models import Base
from peewee import CharField, IntegerField, BooleanField


class Song(Base):
    id = IntegerField(primary_key=True)
    name = CharField()
    album = CharField()
    year = CharField()
    is_processed = BooleanField()
    is_uploaded = BooleanField()
    path_to_song = CharField()
