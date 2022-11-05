import discogs_client

from app import schemas
from app.core import settings


class DiscogsWrapper:
    def __init__(self):
        self.client = discogs_client.Client(
            "Flaccy/0.1", user_token=settings.discogs_token
        )

    def get_album_art(self, song: schemas.Song):
        results = self.client.search(song.album, song.artist)

        r = results.page(1)

        images = [i for i in r[0].images if "images" in r[0]] if len(r) > 0 else []

        if not len(images):
            return None

        return images[0]["uri"]


discogs = DiscogsWrapper()
