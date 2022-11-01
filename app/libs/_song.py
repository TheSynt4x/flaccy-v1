from typing import Any, Dict, List, Optional, Tuple

from mutagen.flac import FLAC

from app import models, schemas


class SongWrapper:
    def _get_song_field(self, flac: FLAC, field_name: str) -> Optional[str]:
        return flac.get(field_name)[0] if len(flac.get(field_name, [])) else None

    def get_song_fields(
        self, flac: FLAC, field_names: List[str] = None
    ) -> Dict[str, Any]:
        if field_names is None:
            field_names = []

        fields: Dict[str, Any] = {}

        for field_name in field_names:
            fields[field_name] = self._get_song_field(flac, field_name)

        return fields

    def get_song_info(self, song_path: str) -> Tuple[schemas.Song, FLAC]:
        flac = FLAC(song_path)

        song = self.get_song_fields(
            flac, ["title", "albumartist", "originalyear", "artist", "album", "date"]
        )

        art = flac.pictures[0].data if len(flac.pictures) else None

        return (
            schemas.Song(
                **{
                    "title": song.get("title"),
                    "artist": song.get("artist") or song.get("albumartist"),
                    "album": song.get("album"),
                    "year": song.get("originalyear") or song.get("date"),
                    "cover": art,
                },
            ),
            flac,
        )

    def process_song(
        self, song: schemas.Song, is_processed: int = 0, is_uploaded: int = 0
    ):
        song_data = {
            "title": song.title,
            "artist": song.artist,
            "album": song.album,
            "year": song.year,
            "is_processed": is_processed,
            "is_uploaded": is_uploaded,
            "source_file": song.source_file,
            "output_file": song.output_file,
        }

        song = models.Song.get_or_create(
            **{
                **song_data,
                "is_processed": is_processed,
                "is_uploaded": is_uploaded,
            }
        )

        return song


song = SongWrapper()
