import discogs_client
import requests

from app import schemas
from app.core import logger, settings


class DiscogsWrapper:
    def __init__(self):
        self.client = discogs_client.Client(
            "Flaccy/0.1", user_token=settings.discogs_token
        )

    def get_artist_information(self, name: str):
        results = self.client.search(name, type="artist")

        results = results.page(0)

        if len(results or []):
            try:
                response = requests.get(
                    results[0].data.get("resource_url")
                    + "?token="
                    + settings.discogs_token
                )
                response.raise_for_status()

                return response.json()
            except requests.HTTPError:
                pass

        return None

    def get_album_art(self, song: schemas.Song):
        if not song.album or not song.artist:
            return

        results = self.client.search(song.album, song.artist)

        results = results.page(0)

        if len(results or []):
            if len(results[0].images or []):
                if "uri" in results[0].images[0]:
                    logger.info("Downloading from discogs")

                    return results[0].images[0]["uri"]

        return None


discogs = DiscogsWrapper()
