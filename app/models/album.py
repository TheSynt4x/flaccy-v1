from typing import List

from peewee import BooleanField, CharField, IntegerField

from app.models.base import Base


class UploadedAlbum(Base):
    id = IntegerField(primary_key=True)
    artist = CharField()
    name = CharField()
    source_path = CharField()
    output_path = CharField()
    is_uploaded = BooleanField()

    @classmethod
    def all(cls: "UploadedAlbum") -> List["UploadedAlbum"]:
        return [album for album in cls.select().dicts()]

    @classmethod
    def get_unuploaded_albums(cls: "UploadedAlbum"):
        return cls.select().where(cls.is_uploaded is False)

    @classmethod
    def get_by_output_path(cls: "UploadedAlbum", output_path: str) -> "UploadedAlbum":
        return cls.select().where(cls.output_path == output_path).get()

    @classmethod
    def update_upload_status(
        cls: "UploadedAlbum", output_path: str, is_uploaded: bool = False
    ) -> "UploadedAlbum":
        s = cls.get_by_output_path(output_path)

        if not s:
            return None

        s.is_uploaded = is_uploaded
        s.save()

        return s
