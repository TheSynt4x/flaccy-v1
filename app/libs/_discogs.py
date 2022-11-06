import discogs_client

from app import schemas
from app.core import logger, settings


class DiscogsWrapper:
    def __init__(self):
        self.client = discogs_client.Client(
            "Flaccy/0.1", user_token=settings.discogs_token
        )

    def get_album_art(self, song: schemas.Song):
        results = self.client.search(song.album, song.artist)

        results = results.page(0)

        if len(results or []):
            if len(results[0].images or []):
                if "uri" in results[0].images[0]:
                    logger.info("Downloading from discogs")

                    return results[0].images[0]["uri"]

        return None


discogs = DiscogsWrapper()
