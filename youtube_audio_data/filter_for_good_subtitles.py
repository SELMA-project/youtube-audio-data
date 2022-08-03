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

from data_io.readwrite_files import read_json, write_jsonl, read_jsonl, write_lines
from misc_utils.buildable import Buildable
from misc_utils.buildable_data import BuildableData
from misc_utils.dataclass_utils import UNDEFINED
from misc_utils.prefix_suffix import BASE_PATHES, PrefixSuffix


@beartype
def parse_youtube_time(self, duration_str) -> float:
    zero = datetime.strptime("00:00:00.000", "%H:%M:%S.%f")

    if len(duration_str.split(":")) == 1:
        seconds = float(duration_str)
    elif len(duration_str.split(":")) == 2:
        seconds = float(
            (datetime.strptime(duration_str, "%M:%S") - zero).total_seconds()
        )
    elif len(duration_str.split(":")) == 3:
        # cause youtube does not count in days but simply in hours like 246:12:12

        hours_str, *minutes_seconds = duration_str.split(":")
        minutes_seconds = ":".join(minutes_seconds)
        hours = int(hours_str)
        time_format = "%M:%S.%f" if "." in duration_str else "%M:%S"
        seconds = float(
            (datetime.strptime(minutes_seconds, time_format) - zero).total_seconds()
            + hours * 60 ** 2
        )
    else:
        print(f"{duration_str=}")
        raise NotImplementedError
    return seconds


@dataclass
class YoutubeSubtitles(BuildableData):
    vtt_file_folder: str = UNDEFINED

    @property
    def name(self):
        return f"youtube_info-jsons_vtt-files"

    @property
    def _is_data_valid(self) -> bool:
        return False

    @staticmethod
    def subtitle_id(display_id: str, lang: str):
        return display_id + "-" + lang

    def _build_data(self) -> Any:
        os.makedirs(self.data_dir, exist_ok=True)
        file = f"{self.data_dir}/subtitle_stats.jsonl"
        if os.path.isfile(file):
            self._already_processed_ids = set(
                [d["display_id"] for d in read_jsonl(file)]
            )
            write_lines(f"{self.data_dir}/already_proccesed.txt",list(self._already_processed_ids))
            print(f"{len(self._already_processed_ids)=}")
        else:
            self._already_processed_ids = set()

        write_jsonl(
            file,
            tqdm(
                self._gen_subtitle_stats(),
                desc=f"processing {self.__class__.__name__}-{self.name}",
                position=1,
            ),
            mode="ab",
        )

    def _process_channel(self, p_info_json: Path, folder: str, channel_id: str):
        d = read_json(str(p_info_json).replace(".vtt", ".info.json"))
        vtt_files = self._get_vtt_files(folder, p_info_json)
        if len(vtt_files) > 0:
            if "duration_string" not in d:
                print(p_info_json)
                print(d)
                print(f'{d["display_id"]} does not have duration string')
                raise AssertionError
            duration_str = d["duration_string"]
            seconds = parse_youtube_time(duration_str)
            for p_vtt in vtt_files:
                raise NotImplementedError("TODO here")
                s_e_t = list(
                    (
                        parse_youtube_time(c.start),
                        parse_youtube_time(c.end),
                        c.text,
                    )
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
                    "start_end_text": s_e_t,
                    "lang": self.lang_from_vtt_file(p_vtt),
                    "audio_duration": seconds,
                    "overall_subtitle_duration": subtitle_duration,
                    "overall_subtitle_len": overall_subtitle_len,
                    "char_per_sec": char_per_sec,
                }

    def _gen_subtitle_stats(self):
        g = (
            (p_vtt, channel_id)
            for channel_id in os.listdir(self.vtt_file_folder)
            for p_vtt in Path(f"{self.vtt_file_folder}/{channel_id}").glob(
                "*.vtt"
            )
        )
        for p_vtt, channel_id in tqdm(g, desc="info-jsons", position=0):
            # TODO: loop over vtt-files load info-jsons via a cached method, assuming that same-video vtt-files + info.json come in a row
                # @lru_cache ?
            folder = f"{self.vtt_file_folder}/{channel_id}"
            display_id = str(p_vtt).split("[")[-1].split("]")[0]
            if display_id not in self._already_processed_ids:
                yield from self._process_channel(p_vtt, folder, channel_id)
                self._already_processed_ids.add(display_id)
            else:
                write_lines(f"{self.data_dir}/known_ids.txt",[display_id],mode="ab")

    def lang_from_vtt_file(self, p_vtt):
        return str(p_vtt).split(".")[-2]

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

    YoutubeSubtitles(
        base_dir=PrefixSuffix("cache_root", "YOUTUBE"),
        # vtt_file_folder="/home/tilo/code/iais_code/youtube-audio-data/resources",
        vtt_file_folder="/nm-raid/audio/work/thimmelsba/data/ASR_DATA/YOUTUBE/YOUTUBE_info_jsons_vtt_files",
    ).build()
