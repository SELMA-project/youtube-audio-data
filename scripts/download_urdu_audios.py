import os
import shutil
from pathlib import Path
from tempfile import NamedTemporaryFile

from data_io.readwrite_files import read_json, write_lines
from misc_utils.processing_utils import exec_command


def collect_urdu_ids():
    path = f"{os.environ['BASE_PATH']}/data/ASR_DATA/YOUTUBE/YOUTUBE_info_jsons_vtt_files/user_tagesschau"
    ids = []
    for p in Path(path).glob("*tagesschau*.info.json"):
        d = read_json(str(p))
        ids.append(d["id"])
    return ids


if __name__ == "__main__":
    resource_dir = f"{os.environ['BASE_PATH']}/data/ASR_DATA/YOUTUBE/urdu_audios"
    with NamedTemporaryFile(prefix="youtube_ids", suffix=".txt") as tmpfile:
        batch_file = tmpfile.name
        ids = collect_urdu_ids()
        write_lines(batch_file, ids)

        os.makedirs(resource_dir, exist_ok=True)
        downloadedarchive_txt = f"{resource_dir}/downloadedarchive.txt"
        cmd = f'cd {resource_dir} && yt-dlp --match-filter !is_live -o "%(title)+.100U-%(id)s.%(ext)s" --write-sub --all-subs --write-info-json --download-archive {downloadedarchive_txt} --batch-file {batch_file} | tee log.log'
        print(f"{cmd}")
        print(exec_command(cmd))
