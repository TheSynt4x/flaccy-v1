from peewee import BooleanField, CharField, IntegerField

from app.models import Base


class Song(Base):
    id = IntegerField(primary_key=True)
    title = CharField()
    artist = CharField()
    album = CharField()
    year = CharField(null=True)
    is_processed = BooleanField()
    is_uploaded = BooleanField()
    source_file = CharField()
    output_file = CharField()

    @classmethod
    def get_by_output_file(cls: "Song", output_file: str) -> "Song":
        return cls.select().where(cls.output_file == output_file).get()

    @classmethod
    def update_upload_status(
        cls: "Song", output_file: str, is_uploaded: bool = False
    ) -> "Song":
        s = cls.get_by_output_file(output_file)

        if not s:
            return None

        s.is_uploaded = is_uploaded
        s.save()

        return s
