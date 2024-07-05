import logging
import os
import subprocess
from socket import gethostname
from typing import Dict, Any
from db import Track

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

FFMPEG = "ffmpeg"
DOCKER_FLAC_VOLUME = "/flac_dir"
DOCKER_MP3_VOLUME = "/mp3_dir"
DEV_BOX = "ad-mbp.lan"
DEV_BOX_FFMPEG = os.path.join(os.path.dirname(os.path.dirname(__file__)), "ffmpeg")


def _convert(flac_path, mp3_path):
    command = [
        FFMPEG, '-i', flac_path, '-f', 'flac', '-b:a', '320k', '-map_metadata', '0', mp3_path
    ]
    subprocess.run(command, check=True)


def convert(flac_path, mp3_path, dest_dir):
    if os.path.exists(mp3_path):
        logging.warning(f"exists: {mp3_path}")
        return
    try:
        _convert(flac_path, mp3_path)
    except Exception as e:
        logging.error(f"ERROR {mp3_path}")
        with open(os.path.join(dest_dir, "ERRORS.out"), "a+") as f:
            f.write(f"{mp3_path}\n")








# def from_flac(file_path: str) -> 'Track':
#     metadata = get_flac_metadata(file_path)
#     return Track(
#         artist=metadata.get('artist'),
#         title=metadata.get('title'),
#         album=metadata.get('album'),
#         bitrate=metadata.get('bitrate'),
#         genre=metadata.get('genre'),
#         year=metadata.get('date'),  # or 'year' depending on your metadata
#         duration=metadata.get('duration'),  # might need to calculate duration separately
#         filename=file_path
#     )


def add_track_to_db(flac_path, mp3_path):
    print(f"{flac_path}: {mp3_path}")
    # metadata = get_flac_metadata(flac_path)
    # logging.info(metadata)
    # metadata = get_flac_metadata(mp3_path)
    # logging.info(metadata)
    track = Track(filename=flac_path)
    metadata = track.from_flac(flac_path)
    print(metadata)
    print(f"{track.to_json()}")
    exit()


def convert_flac_to_mp3(source_dir, dest_dir):
    print(f"Converting flac to mp3 {source_dir} {dest_dir}")
    for root, dirs, files in os.walk(source_dir):
        for file in files:
            logging.info(f"Converting {file}")
            if file.lower().endswith('.flac'):
                flac_path = os.path.join(root, file)
                relative_path = os.path.relpath(root, source_dir)
                mp3_dir = os.path.join(dest_dir, relative_path)
                os.makedirs(mp3_dir, exist_ok=True)
                mp3_path = os.path.join(mp3_dir, os.path.splitext(file)[0] + '.mp3')
                convert(flac_path, mp3_path, dest_dir)
                add_track_to_db(flac_path, mp3_path)
                exit()
            exit()




if __name__ == '__main__':

    # run for local development, no docker, no global ffmpeg installed
    if gethostname() == DEV_BOX:
        globals()["FFMPEG"] = DEV_BOX_FFMPEG
        convert_flac_to_mp3("/Users/ad/Projects/music_service/test_data",
                            "/Users/ad/Projects/music_service/test_data_out")
    else:
        # docker running on the nas with ffmpeg globally installed
        convert_flac_to_mp3(DOCKER_FLAC_VOLUME, DOCKER_MP3_VOLUME)
