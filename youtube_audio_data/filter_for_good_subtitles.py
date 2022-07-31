import glob
import os
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any

import webvtt
from beartype import beartype
from tqdm import tqdm
from webvtt import WebVTT, Caption

from data_io.readwrite_files import read_json, write_jsonl
from misc_utils.buildable import Buildable
from misc_utils.buildable_data import BuildableData
from misc_utils.dataclass_utils import UNDEFINED
from misc_utils.prefix_suffix import BASE_PATHES, PrefixSuffix

zero = datetime.strptime("00:00:00.000", "%H:%M:%S.%f")


@beartype
def parse_time(s: str) -> float:
    return (datetime.strptime(s, "%H:%M:%S.%f") - zero).total_seconds()


@dataclass
class GoodSubtitles(BuildableData):
    vtt_file_folder: str = UNDEFINED

    @property
    def name(self):
        return f"youtube_info-jsons_vtt-files"

    @property
    def _is_data_valid(self) -> bool:
        return False

    def _build_data(self) -> Any:
        os.makedirs(self.data_dir, exist_ok=True)
        write_jsonl(
            f"{self.data_dir}/subtitle_stats.jsonl",
            tqdm(
                self._gen_subtitle_stats(),
                desc=f"processing {self.__class__.__name__}-{self.name}",
            ),
        )

    def _gen_subtitle_stats(self):
        for channel_id in os.listdir(self.vtt_file_folder):
            folder = f"{self.vtt_file_folder}/{channel_id}"
            for p_info_json in Path(folder).glob("*.info.json"):
                d = read_json(str(p_info_json).replace(".vtt", ".info.json"))
                vtt_files = self._get_vtt_files(folder, p_info_json)
                if len(vtt_files) > 0:
                    if "duration_string" not in d:
                        print(p_info_json)
                        print(d)
                        print(f'{d["display_id"]} does not have duration string')
                        raise AssertionError
                        continue
                    duration_str = d["duration_string"]
                    if len(duration_str.split(":")) == 1:
                        duration = int(duration_str)
                    elif len(duration_str.split(":")) == 2:
                        duration = (
                            datetime.strptime(duration_str, "%M:%S")
                            - datetime(1900, 1, 1, 0, 0, 0)
                        ).total_seconds()
                    elif len(duration_str.split(":")) == 3:
                        duration = (
                            datetime.strptime(duration_str, "%H:%M:%S")
                            - datetime(1900, 1, 1, 0, 0, 0)
                        ).total_seconds()
                    else:
                        print(f"{duration_str=}")
                        raise NotImplementedError
                    for p_vtt in vtt_files:
                        s_e_t = list(
                            (parse_time(c.start), parse_time(c.end), c.text)
                            for c in webvtt.read(str(p_vtt))
                        )
                        subtitle_duration = sum((e - s for s, e, _ in s_e_t))
                        overall_subtitle_len = sum((len(t) for _, _, t in s_e_t))
                        char_per_sec = overall_subtitle_len / subtitle_duration
                        yield {
                            "channel_id": channel_id,
                            "display_id": d["display_id"],
                            "info_json": str(p_info_json),
                            "vtt_file": str(p_vtt),
                            "audio_duration": duration,
                            "overall_subtitle_duration": subtitle_duration,
                            "overall_subtitle_len": overall_subtitle_len,
                            "char_per_sec": char_per_sec,
                        }

    def _get_vtt_files(self, folder, p_info_json):
        s = p_info_json.name.replace(".info.json", "")
        patt = f"{glob.escape(s)}*.vtt"
        vtt_files = list(p_vtt for p_vtt in Path(folder).glob(patt))
        return vtt_files


if __name__ == "__main__":

    base_path = os.environ["BASE_PATH"]
    # base_path = f"/home/tilo"
    cache_root = f"{base_path}/data/cache"
    BASE_PATHES["base_path"] = base_path
    BASE_PATHES["cache_root"] = cache_root
    BASE_PATHES["raw_data"] = PrefixSuffix("cache_root", "RAW_DATA")

    GoodSubtitles(
        base_dir=PrefixSuffix("cache_root", "YOUTUBE"),
        # vtt_file_folder="/home/tilo/code/iais_code/youtube-audio-data/resources",
        vtt_file_folder="/nm-raid/audio/work/thimmelsba/data/ASR_DATA/YOUTUBE/YOUTUBE_info_jsons_vtt_files",
    ).build()
