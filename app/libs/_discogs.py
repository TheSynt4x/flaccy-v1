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

        r = results.page(0)

        if not len(r):
            r = results.page(1)

        if not len(r):
            return None

        images = [i for i in results[0].images]

        if not len(images):
            return None

        return images[0]["uri"]


discogs = DiscogsWrapper()
