import os
import shutil
from pathlib import Path
from tempfile import NamedTemporaryFile

from data_io.readwrite_files import read_json, write_lines
from misc_utils.processing_utils import exec_command


def collect_urdu_ids():
    path = f"{os.environ['BASE_PATH']}/data/ASR_DATA/YOUTUBE/YOUTUBE_info_jsons_vtt_files/c_KainaatAstronomyinUrdu"
    ids = []
    for p in Path(path).glob("*.ur.vtt"):
        info_json = str(p).replace("ur.vtt", "info.json")
        d = read_json(info_json)
        ids.append(d["id"])
    return ids


if __name__ == "__main__":
    resource_dir = f"{os.environ['BASE_PATH']}/data/ASR_DATA/YOUTUBE/urdu_audios"
    with NamedTemporaryFile(
        prefix="youtube_ids", suffix=".txt", delete=True
    ) as tmpfile:
        batch_file = tmpfile.name
        ids = collect_urdu_ids()
        write_lines(batch_file, ids)

        os.makedirs(resource_dir, exist_ok=True)
        downloadedarchive_txt = f"{resource_dir}/downloadedarchive.txt"
        post_processor = f'--postprocessor-args "ffmpeg:-c:a libopus -ar 16000 -ac 1"'
        cmd = f'cd {resource_dir} && yt-dlp --match-filter !is_live -o "%(title)+.100U-%(id)s.%(ext)s" --write-sub --all-subs --write-info-json --download-archive {downloadedarchive_txt} --extract-audio --audio-format opus -f ba {post_processor} --batch-file {batch_file} | tee log.log'
        print(f"{cmd}")
        print(exec_command(cmd))
