import itertools
import os
import shutil
from pathlib import Path

from tqdm import tqdm

from data_io.readwrite_files import read_json, write_lines
from misc_utils.processing_utils import exec_command


def collect_video_ids():
    path = f"{os.environ['BASE_PATH']}/data/ASR_DATA/YOUTUBE/DW_channels/dwrussian"
    ids = []
    newest = itertools.islice(
        sorted(
            tqdm(Path(path).glob("*.info.json"), desc="sorting ids"),
            key=os.path.getmtime,
        ),
        100,
    )

    for p in newest:
        d = read_json(str(p))
        ids.append(d["id"])
    return ids


if __name__ == "__main__":
    # batch_file = "tagesschau_ids.txt"
    ids = collect_video_ids()
    print(f"{ids=}")
    resource_dir = f"{os.environ['BASE_PATH']}/data/ASR_DATA/YOUTUBE/russian_videos"

    os.makedirs(resource_dir, exist_ok=True)
    batch_file = f"{resource_dir}/video_ids.txt"
    write_lines(batch_file, ids)

    downloadedarchive_txt = f"{resource_dir}/downloadedarchive.txt"
    subtitles_but_no_chats = (
        " --write-sub --compat-options no-live-chat --sub-langs all,-live_chat "
    )
    cmd = f'cd {resource_dir} && yt-dlp --write-info-json {subtitles_but_no_chats} --match-filter !is_live -o "%(title)+.100U-%(id)s.%(ext)s" --download-archive {downloadedarchive_txt} --batch-file {batch_file} | tee log.log'
    print(f"{cmd}")
    print(exec_command(cmd))

    # paths = sorted(Path(dirpath).iterdir(), key=os.path.getmtime)

    # files = list(filter(os.path.isfile, glob.glob(search_dir + "*")))
    # files.sort(key=lambda x: os.path.getmtime(x))
