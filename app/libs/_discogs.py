import discogs_client

from app import schemas
from app.core import settings


class DiscogsWrapper:
    def __init__(self):
        self.client = discogs_client.Client(
            "Flaccy/0.1", user_token=settings.discogs_token
        )

    def get_album_art(self, song: schemas.Song):
        results = self.client.search(
            song.title, album=song.album, artist=song.artist, year=song.year
        )

        results = results.page(1)

        images = [i for i in results[0].images]

        if not len(images):
            return None

        return images[0]["uri"]


discogs = DiscogsWrapper()
