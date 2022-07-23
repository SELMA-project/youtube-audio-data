import itertools
import os
import shutil
from dataclasses import dataclass, field
from pathlib import Path
from typing import Union, Iterable, ClassVar, Iterator

from langdetect import detect as lang_detect

from tqdm import tqdm

from audio_data_collection.youtube.filter_youtube_results import (
    LangDetectedYoutubeResults,
    is_good_lang,
    GoodSearchResults,
)
from data_io.readwrite_files import (
    read_jsonl,
    write_lines,
    read_json,
    write_jsonl,
    read_lines,
)
from misc_utils.cached_data import (
    CachedData,
    PrefixSuffix,
)
from misc_utils.cached_data_specific import ContinuedCachedDicts, ContinuedCachedData
from misc_utils.dataclass_utils import _UNDEFINED, UNDEFINED
from misc_utils.prefix_suffix import BASE_PATHES
from misc_utils.processing_utils import exec_command
from misc_utils.utils import just_try


@dataclass
class TODOResults(ContinuedCachedDicts):
    """

    """
    results: Union[_UNDEFINED, GoodSearchResults] = UNDEFINED
    youtube_subtitles_dir:Union[_UNDEFINED,str]=UNDEFINED
    cache_base: PrefixSuffix = field(default_factory=lambda: BASE_PATHES["youtube_root"])

    def _build_already_got_subtitles(self) -> list[str]:
        id_suffixes_file = self.prefix_cache_dir("id_suffixes.txt")
        cmd = f'ls -alth {self.youtube_subtitles_dir} | rg -o "(?:\-.{{11}}|\[.{{11}}\])\.info\.json" > {id_suffixes_file}'
        print(f"{cmd=}")
        print(exec_command(cmd))

        def clean_suffix(s):
            return (
                s.replace(".info.json", "")
                .replace("[", "")
                .replace("]", "")
                .replace("-", "")
            )

        already_got_subtitles = list(
            set(clean_suffix(s) for s in read_lines(id_suffixes_file))
        )
        assert len(already_got_subtitles) > 0
        write_lines(self.prefix_cache_dir("already_got_ids.txt"), already_got_subtitles)
        return already_got_subtitles

    def generate_dicts_to_cache(self) -> Iterator[dict]:
        already_got_subtitles = self._build_already_got_subtitles()
        todo_results = [
            d
            for d in tqdm(self.results, desc="filter for new ids")
            if d["id"] not in already_got_subtitles
        ]
        yield from todo_results


@dataclass
class UrlsToDownload(ContinuedCachedData):
    """
    moving info.json and vtt files and writing batch-file with urls
    """

    todo_results: TODOResults = UNDEFINED
    youtube_subtitles_dir: str = UNDEFINED
    youtube_audio_dir: str = UNDEFINED
    cache_base: PrefixSuffix = field(default_factory=lambda: BASE_PATHES["youtube_root"])

    @property
    def batch_file(self) -> str:
        return self.prefix_cache_dir("urls.txt")

    def continued_build_cache(self) -> None:
        for p in tqdm(
            itertools.chain(
                Path(self.youtube_audio_dir).glob("*.info.json"),
                Path(self.youtube_audio_dir).glob("*.vtt"),
            ),
            desc="moving from audio to subtitles dir",
        ):
            assert str(p).startswith(self.youtube_audio_dir)
            shutil.move(
                str(p),
                str(p).replace(self.youtube_audio_dir, self.youtube_subtitles_dir),
            )

        # if just_try(lambda: lang_detect(d["title"]), default="no-lang") == "de"]
        base_url = "https://www.youtube.com"
        urls = list(f'{base_url}{d["url_suffix"]}' for d in self.todo_results)
        write_lines(self.batch_file, urls)


base_path = os.environ["BASE_PATH"]

if __name__ == "__main__":
    BASE_PATHES["base_path"] = base_path
    BASE_PATHES["youtube_root"] = PrefixSuffix("base_path","data/ASR_DATA/YOUTUBE")

    base_dir = f"{base_path}/data/ASR_DATA/YOUTUBE_audios"
    urls = UrlsToDownload(todo_results=LangDetectedYoutubeResults()).build()
    batch_file = urls.batch_file
    # batch_file = write_batch_file()
    # post_processor=f"--postprocessor-args \"ffmpeg:-q:a 0 -ac 1 -ar 16000\""
    # post_processor = f'--postprocessor-args "ffmpeg:-c:a libopus -ar 16000 -ac 1"'
    resource_dir = base_dir
    subtitles_only_dir = f"{base_path}/data/ASR_DATA/YOUTUBE_subtitles"
    os.makedirs(subtitles_only_dir, exist_ok=True)
    # downloadedarchive_txt = "downloadedarchive.txt"
    # cmd = f'cd {resource_dir} && yt-dlp --match-filter !is_live -o "%(title)+.100U-%(id)s.%(ext)s" --write-sub --all-subs --write-info-json --download-archive {downloadedarchive_txt} --extract-audio --audio-format opus -f ba {post_processor} --batch-file {batch_file} | tee log.log'
    cmd = f'cd {subtitles_only_dir} && yt-dlp --match-filter !is_live -o "%(title)+.100U-%(id)s.%(ext)s" --write-sub --all-subs --write-info-json --skip-download --batch-file {batch_file} | tee log.log'
    print(f"{cmd}")
    print(exec_command(cmd))

"""
ll $BASE_PATH/data/ASR_DATA/YOUTUBE_audios | rg "\.opus" | wc -l
6700 in 24 h

Every 10,0s: ls -alht | rg '\.info\.json' | wc -l 
Sun Jan  9 15:55:34 2022
26

cat log.log | rg "\.info\.json" | wc -l

"""
