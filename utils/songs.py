import glob
from pathlib import Path


def get_song_files(library):
    files = []

    for filename in glob.iglob(f"{library['source']}/**/*", recursive=True):
        ending = Path(filename).suffix
        if ending in library["formats"]:
            files.append(filename)

    return files
