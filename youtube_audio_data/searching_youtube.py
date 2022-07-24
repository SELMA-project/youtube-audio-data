import itertools
import sys
from pathlib import Path

from misc_utils.cached_data_specific import ContinuedCachedDicts
from misc_utils.processing_utils import iterable_to_batches
from misc_utils.utils import retry
from ml4audio.text_processing.character_mappings.character_mapping import (
    CHARACTER_MAPPINGS,
)

import os
import re
import string
from dataclasses import dataclass, field
from time import sleep
from typing import Optional, Iterable

import requests
import urllib.parse
import json

from beartype import beartype
from tqdm import tqdm

from data_io.readwrite_files import (
    write_jsonl,
    read_jsonl,
    read_lines,
    write_lines,
    read_json,
)

filters = {
    "subtitles&thisyear": "&sp=EgYIBRABKAE%253D",
    "subtitles&thismonth": "&sp=EgYIBBABKAE%253D",
    "subtitles&thisweek": "&sp=EgQIAygB",
    # "subtitles": "&sp=EgQQASgB",
    "subtitles": "&sp=EgIoAQ%253D%253D",
}


def ngrams(sequence, n):
    """
    STOLEN from: speechbrain/lm/counting.py
    Produce all Nth order N-grams from the sequence.

    This will generally be used in an N-gram counting pipeline.

    Arguments
    ---------
    sequence : iterator
        The sequence from which to produce N-grams.
    n : int
        The order of N-grams to produce

    Yields
    ------
    tuple
        Yields each ngram as a tuple.

    Example
    -------
    >>> for ngram in ngrams("Brain", 3):
    ...     print(ngram)
    ('B', 'r', 'a')
    ('r', 'a', 'i')
    ('a', 'i', 'n')

    """
    if n <= 0:
        raise ValueError("N must be >=1")
    # Handle the unigram case specially:
    if n == 1:
        for token in sequence:
            yield (token,)
        return
    iterator = iter(sequence)
    history = []
    for hist_length, token in enumerate(iterator, start=1):
        history.append(token)
        if hist_length == n - 1:
            break
    else:  # For-else is obscure but fits here perfectly
        return
    for token in iterator:
        yield tuple(history) + (token,)
        history.append(token)
        del history[0]
    return


@dataclass
class YoutubeSearch:
    """
    based on: https://github.com/joetats/youtube_search/blob/master/youtube_search/__init__.py
    """

    search_terms: str
    search_fitler: Optional[str] = None
    wait_before_search: float = 1.0

    @beartype
    def search(self) -> list:
        sleep(self.wait_before_search)
        url = self._build_search_url()

        def get_results():
            response = requests.get(url).text
            assert "ytInitialData" in response
            results = self._parse_html(response)
            return results

        results = retry(get_results, num_retries=3, default=[], do_raise=False)
        return results

    def _build_search_url(self):
        encoded_search = urllib.parse.quote_plus(self.search_terms)
        BASE_URL = "https://youtube.com"
        url = f"{BASE_URL}/results?search_query={encoded_search}{filters.get(self.search_fitler, '')}"
        return url

    # TODO unused?
    # def get_channel_url_suffix(
    #     self,
    # ) -> Optional[str]:
    #     url = self._build_search_url()
    #
    #     def get_results():
    #         response = requests.get(url).text
    #         videos = self._parse_videos(response)
    #         channel = [v for v in videos if "channelRenderer" in v]
    #         return channel[0]["channelRenderer"]["navigationEndpoint"]["browseEndpoint"][
    #             "canonicalBaseUrl"
    #         ]
    #
    #     results = retry(get_results, num_retries=3, default=None, do_raise=False)
    #     return results

    def _parse_html(self, response: str):
        """
        returns at max 20 results, cause simply parses html WITHOUT scrolling!
        see: https://github.com/joetats/youtube_search/issues/19
        """
        results = []
        videos = self._parse_videos(response)
        valid_videos = [video for video in videos if "videoRenderer" in video.keys()]
        for rank, video in enumerate(valid_videos):
            res = {}
            video_data = video.get("videoRenderer", {})
            res["id"] = video_data.get("videoId", None)
            res["thumbnails"] = [
                thumb.get("url", None)
                for thumb in video_data.get("thumbnail", {}).get("thumbnails", [{}])
            ]
            res["title"] = (
                video_data.get("title", {}).get("runs", [[{}]])[0].get("text", None)
            )
            res["long_desc"] = (
                video_data.get("descriptionSnippet", {})
                .get("runs", [{}])[0]
                .get("text", None)
            )
            res["channel"] = (
                video_data.get("longBylineText", {})
                .get("runs", [[{}]])[0]
                .get("text", None)
            )
            res["duration"] = video_data.get("lengthText", {}).get("simpleText", 0)
            res["views"] = video_data.get("viewCountText", {}).get("simpleText", 0)
            res["publish_time"] = video_data.get("publishedTimeText", {}).get(
                "simpleText", 0
            )
            res["url_suffix"] = (
                video_data.get("navigationEndpoint", {})
                .get("commandMetadata", {})
                .get("webCommandMetadata", {})
                .get("url", None)
            )
            res["rank"] = rank
            results.append(res)
        return results

    def _parse_videos(self, response: str):
        start = response.index("ytInitialData") + len("ytInitialData") + 3
        end = response.index("};", start) + 1
        json_str = response[start:end]
        data = json.loads(json_str)
        videos = data["contents"]["twoColumnSearchResultsRenderer"]["primaryContents"][
            "sectionListRenderer"
        ]["contents"][0]["itemSectionRenderer"]["contents"]
        return videos


def gen_search_phrase_ngrams(text: str):
    text = CHARACTER_MAPPINGS["no_punct"](text)
    text = re.sub("\s+", " ", text).strip(" ")

    n = 5
    # g=itertools.islice(ngrams(text.split(" "), n=n),None,None,4)
    tokens = text.split(" ")
    if len(tokens) > 5:
        g = iterable_to_batches(tokens, batch_size=5)
        kgrams = list(g)
        len_last_kgram = len(kgrams[-1])
        if len_last_kgram < n:
            kgrams[-1] = tokens[-n:-len_last_kgram] + kgrams[-1]
        assert all((len(ng) == n for ng in kgrams))
        phrases = [" ".join(ng) for ng in kgrams]

    else:
        phrases = [text]

    yield from phrases


def is_new(eid: str, sett: list) -> bool:
    if eid in sett:
        # print(f"{eid} is not new!")
        return False
    else:
        sett.append(eid)
        return True


def write_jsonl_batch_and_yield(batch, file):
    write_jsonl(file, batch, mode="ab")
    return batch


@dataclass
class BootstrappedYoutubeSearch:
    """
    making it ContinuedCachedDicts?
    """

    max_rank: dict[int, int] = field(default_factory=lambda: {0: 10}, repr=False)
    max_depth: int = 1
    known_ids: list[str] = field(default_factory=lambda: list(), repr=False)
    known_searches: list[str] = field(default_factory=lambda: list(), repr=False)
    search_filter: Optional[str] = "subtitles&thismonth"
    # lang: str = "en"
    results_file: str = "results.jsonl"
    searches_file: str = "search_phrases.txt"

    @beartype
    def run(self, titles: list[str]):
        if os.path.isfile(self.results_file):
            self.known_ids = [d["id"] for d in read_jsonl(self.results_file)]
        else:
            print(f"did NOT find {self.results_file}!!!")
        if os.path.isfile(self.searches_file):
            self.known_searches = list(
                set([json.dumps(d) for d in read_jsonl(self.searches_file)])
            )
            write_jsonl(
                self.searches_file,
                tqdm(
                    (json.loads(s) for s in self.known_searches),
                    desc="writing deduplicated search-file",
                ),
            )
        print(
            f"resuming from {len(self.known_ids)} results and {len(self.known_searches)} known_searches"
        )
        search_phrases = [
            sp for title in titles for sp in gen_search_phrase_ngrams(title)
        ]
        search_phrases = list(set(search_phrases))

        search_phrases = [
            {"phrase": sp, "filter": self.search_filter} for sp in search_phrases
        ]
        print(
            f"created {len(search_phrases)} initial search_phrases from {len(titles)} titles"
        )
        self._bootstrapped_searching(search_phrases)

    # def _is_valid_lang(self, title: str):
    #     return just_try(lambda: lang_detect(title), default="no-lang") == self.lang
    #
    # def _is_valid(self, title: str, depth: int):
    #     valid_letters = has_sufficient_valid_letters(title, self.lang)
    #     if depth == 0:
    #         return valid_letters
    #     else:
    #         return valid_letters and self._is_valid_lang(title)
    #
    def _generate_new_results(
        self, raw_search_phrases: list[dict[str, str]], depth: int = 0
    ) -> list[dict]:
        def gen_raw_results(new_phrases_only: Iterable[dict[str, str]]):

            for d in tqdm(new_phrases_only, desc=f"searching in depth {depth}"):
                phrase = d["phrase"]
                for r in YoutubeSearch(
                    phrase,
                    search_fitler=d["filter"],
                    wait_before_search=0.1,
                ).search():
                    yield r
                # write_jsonl(self.searches_file, [phrase], mode="ab")

        search_phrases = [
            s for s in raw_search_phrases if is_new(json.dumps(s), self.known_searches)
        ]
        write_jsonl(self.searches_file, search_phrases, mode="ab")

        raw_results = list(gen_raw_results(search_phrases))
        # results = filter(lambda d: is_known_lang(d["title"]), raw_results) # language classification quality too bad!
        new_ones_only = list(
            filter(lambda d: is_new(d["id"], self.known_ids), raw_results)
        )
        # valid_ones_only = list(
        #     d for d in new_ones_only if self._is_valid(d["title"], depth)
        # )
        print(
            f"depth {depth},new / raw results: {len(new_ones_only)} / {len(raw_results)}; new / raw search-phrases {len(search_phrases)} / {len(raw_search_phrases)}"
        )
        return new_ones_only

    def _bootstrapped_searching(self, initial_search_phrases: list[dict[str, str]]):
        """
        nothing recursive, just "bootstrapped"
        """
        search_phrases = initial_search_phrases
        for depth in range(self.max_depth):
            new_results = self._generate_new_results(search_phrases, depth)
            write_jsonl(self.results_file, new_results, mode="ab")
            new_search_phrases = self._generate_search_phrases(new_results, depth)
            search_phrases = new_search_phrases

    def _generate_search_phrases(
        self, raw_results: list[dict], depth: int
    ) -> list[dict[str, str]]:
        def is_valid_for_phrase_generation(d) -> bool:
            return d["rank"] <= self.max_rank.get(depth, 1)

        valid_results = list(filter(is_valid_for_phrase_generation, raw_results))

        def gen_search_phrases_for_results(res: list):
            for d in res:
                for sp in [
                    p
                    for kk in ["title", "channel"]
                    for p in gen_search_phrase_ngrams(d[kk])
                ]:
                    search = {"phrase": sp, "filter": self.search_filter}
                    yield search

        all_search_phrases = list(gen_search_phrases_for_results(valid_results))
        # search_phrases = [
        #     s for s in all_search_phrases if is_new(json.dumps(s), self.known_searches)
        # ]
        # print(
        #     f"depth {depth}, phrases: {len(valid_results)}/{len(raw_results)} valid/raw-results; "
        #     f"{len(search_phrases)}/{len(all_search_phrases)} new/all-search_phrases"
        # )
        return all_search_phrases


# if __name__ == "__main__":
#     text = "this is a test for whomever whatever"
#     # n_grams = list(gen_search_phrase_ngrams(text))
#     # print(n_grams)
#     o = YoutubeSearch(search_terms="CNN", wait_before_search=0.0)
#     print(o.get_channel_url_suffix())


if __name__ == "__main__":
    base_dir = "/nm-raid/audio/work/thimmelsba/data/ASR_DATA/YOUTUBE_info_jsons"
    youtube_search_dir = (
        "/nm-raid/audio/work/thimmelsba/data/ASR_DATA/YOUTUBE_SEARCHING"
    )
    searcher = BootstrappedYoutubeSearch(
        search_filter="subtitles",
        max_rank={0: 10, 1: 3},
        max_depth=1,
        results_file=f"{youtube_search_dir}/results.jsonl",
        searches_file=f"{youtube_search_dir}/search_phrases.txt",
    )
    done_file = f"{youtube_search_dir}/done_channels.txt"
    if os.path.isfile(done_file):
        done_channels = list(read_lines(done_file))
    else:
        done_channels = []

    todo = (s for s in search_channels() if s not in done_channels)
    for channel_dir in todo:
        g = (read_json(str(p))["title"] for p in Path(channel_dir).glob("*info.json"))
        titles = list(
            t
            for t in tqdm(
                g, desc=f"collecting titles for {channel_dir.replace(base_dir,'')}"
            )
        )
        print(f"found {len(titles)} for {channel_dir}")
        searcher.run(titles)
        write_lines(done_file, [channel_dir], mode="ab")

"""
cat /nm-raid/audio/work/thimmelsba/data/ASR_DATA/YOUTUBE_SEARCHING/results.jsonl | wc -l
1503051
"""
