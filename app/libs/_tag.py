from mutagen.easyid3 import EasyID3
from mutagen.flac import FLAC
from mutagen.id3 import APIC, ID3

from app import schemas


class TagWrapper:
    def tag(self, flac: FLAC, song: schemas.Song):
        mp3 = EasyID3(song.output_file)

        for tag in flac.keys():
            if tag in list(mp3.valid_keys.keys()):
                mp3[tag] = flac[tag]

        mp3.save()

        mp3_audio = ID3(song.output_file)  # in case we want to add a pic

        if song.cover:
            self.set_apic(mp3_audio, song.cover)

        return mp3_audio

    def set_apic(self, mp3_audio, data: str):
        mp3_audio["APIC"] = APIC(
            encoding=0, mime="image/png", type=3, desc="Cover", data=data
        )

        mp3_audio.save()


tag = TagWrapper()
