# flaccy-v1

Convert FLAC files to MP3 files of any quality with auto FTP capabilities.

## Why?

This project solves my pain-point of organizing, structuring, finding cover art, etc for my music. Most of the FLAC audio comes fully tagged and with images. We can use that to our advantage when converting these files to MP3.


## How to use

### Requirements

1. pipenv
2. ffmpeg installed and added to your PATH

### Setting up

```
git clone https://github.com/TheSynt4x/flaccy-v1.git

cd flaccy-v1

pipenv shell

python main.py setup

python main.py sync --full
```

