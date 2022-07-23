import itertools
import os.path
import string
from collections import Counter
from dataclasses import dataclass, field
from typing import Any, Iterator, Iterable, Union, ClassVar

from tqdm import tqdm
from langdetect import detect as lang_detect

from data_io.readwrite_files import read_jsonl, write_jsonl

from misc_utils.buildable import Buildable
from misc_utils.cached_data import (
    CachedData,
    BASE_PATHES,
    PrefixSuffix,
)
from misc_utils.cached_data_specific import ContinuedCachedDicts
from misc_utils.dataclass_utils import _UNDEFINED, UNDEFINED
from misc_utils.utils import just_try

# fmt: off
vocabs=[
    {"lang": "de", "vocab": {"<pad>": 0, "<s>": 1, "</s>": 2, "<unk>": 3, "|": 4, "'": 5, "-": 6, "A": 7, "B": 8, "C": 9, "D": 10, "E": 11, "F": 12, "G": 13, "H": 14, "I": 15, "J": 16, "K": 17, "L": 18, "M": 19, "N": 20, "O": 21, "P": 22, "Q": 23, "R": 24, "S": 25, "T": 26, "U": 27, "V": 28, "W": 29, "X": 30, "Y": 31, "Z": 32, "Ä": 33, "Í": 34, "Ó": 35, "Ö": 36, "Ü": 37}},
    {"lang": "en", "vocab": {"<pad>": 0, "<s>": 1, "</s>": 2, "<unk>": 3, "|": 4, "'": 5, "-": 6, "A": 7, "B": 8, "C": 9, "D": 10, "E": 11, "F": 12, "G": 13, "H": 14, "I": 15, "J": 16, "K": 17, "L": 18, "M": 19, "N": 20, "O": 21, "P": 22, "Q": 23, "R": 24, "S": 25, "T": 26, "U": 27, "V": 28, "W": 29, "X": 30, "Y": 31, "Z": 32}},
    {"lang": "es", "vocab": {"<pad>": 0, "<s>": 1, "</s>": 2, "<unk>": 3, "|": 4, "'": 5, "-": 6, "A": 7, "B": 8, "C": 9, "D": 10, "E": 11, "F": 12, "G": 13, "H": 14, "I": 15, "J": 16, "K": 17, "L": 18, "M": 19, "N": 20, "O": 21, "P": 22, "Q": 23, "R": 24, "S": 25, "T": 26, "U": 27, "V": 28, "W": 29, "X": 30, "Y": 31, "Z": 32, "Á": 33, "É": 34, "Í": 35, "Ñ": 36, "Ó": 37, "Ö": 38, "Ú": 39, "Ü": 40}},
    {"lang": "fr", "vocab": {"<pad>": 0, "<s>": 1, "</s>": 2, "<unk>": 3, "|": 4, "'": 5, "-": 6, "A": 7, "B": 8, "C": 9, "D": 10, "E": 11, "F": 12, "G": 13, "H": 14, "I": 15, "J": 16, "K": 17, "L": 18, "M": 19, "N": 20, "O": 21, "P": 22, "Q": 23, "R": 24, "S": 25, "T": 26, "U": 27, "V": 28, "W": 29, "X": 30, "Y": 31, "Z": 32, "À": 33, "Á": 34, "Â": 35, "Ä": 36, "Ç": 37, "È": 38, "É": 39, "Ê": 40, "Ë": 41, "Í": 42, "Î": 43, "Ï": 44, "Ñ": 45, "Ó": 46, "Ô": 47, "Ö": 48, "Ù": 49, "Ú": 50, "Û": 51, "Ü": 52, "Ć": 53, "Č": 54, "Ō": 55, "Œ": 56, "Š": 57, "Ș": 58}},
    {"lang": "pt", "vocab": {"<pad>": 0, "<s>": 1, "</s>": 2, "<unk>": 3, "|": 4, "'": 5, "-": 6, "A": 7, "B": 8, "C": 9, "D": 10, "E": 11, "F": 12, "G": 13, "H": 14, "I": 15, "J": 16, "K": 17, "L": 18, "M": 19, "N": 20, "O": 21, "P": 22, "Q": 23, "R": 24, "S": 25, "T": 26, "U": 27, "V": 28, "W": 29, "X": 30, "Y": 31, "Z": 32, "À": 33, "Á": 34, "Â": 35, "Ã": 36, "Ç": 37, "É": 38, "Ê": 39, "Í": 40, "Ó": 41, "Ô": 42, "Õ": 43, "Ú": 44, "Ü": 45}},
    {"lang": "ru", "vocab": {"<pad>": 0, "<s>": 1, "</s>": 2, "<unk>": 3, "|": 4, "-": 5, "Ё": 6, "А": 7, "Б": 8, "В": 9, "Г": 10, "Д": 11, "Е": 12, "Ж": 13, "З": 14, "И": 15, "Й": 16, "К": 17, "Л": 18, "М": 19, "Н": 20, "О": 21, "П": 22, "Р": 23, "С": 24, "Т": 25, "У": 26, "Ф": 27, "Х": 28, "Ц": 29, "Ч": 30, "Ш": 31, "Щ": 32, "Ъ": 33, "Ы": 34, "Ь": 35, "Э": 36, "Ю": 37, "Я": 38}},
    {"lang": "it", "vocab": {"<pad>": 0, "<s>": 1, "</s>": 2, "<unk>": 3, "|": 4, "'": 5, "-": 6, "A": 7, "B": 8, "C": 9, "D": 10, "E": 11, "F": 12, "G": 13, "H": 14, "I": 15, "J": 16, "K": 17, "L": 18, "M": 19, "N": 20, "O": 21, "P": 22, "Q": 23, "R": 24, "S": 25, "T": 26, "U": 27, "V": 28, "W": 29, "X": 30, "Y": 31, "Z": 32, "À": 33, "Á": 34, "È": 35, "É": 36, "Ì": 37, "Í": 38, "Ò": 39, "Ó": 40, "Ù": 41, "Ú": 42, "Š": 43}}
]
# fmt: on
lang2vocabs = {d["lang"]: d["vocab"] for d in vocabs}

languages = [
    s.strip(" ")
    for s in "af, ar, bg, bn, ca, cs, cy, da, de, el, en, es, et, fa, fi, fr, gu, he, hi, hr, hu, id, it, ja, kn, ko, lt, lv, mk, ml, mr, ne, nl, no, pa, pl, pt, ro, ru, sk, sl, so, sq, sv, sw, ta, te, th, tl, tr, uk, ur, vi, zh-cn, zh-tw".split(
        ","
    )
]


@dataclass
class ResultFilter(Buildable):
    langs: list[str]
    lower_limit_proportion: float = 0.75

    vocab_letters: set[str] = field(init=False, repr=False)

    def _build_self(self) -> Any:
        self.vocab_letters = set(
            [l.lower() for lang in self.langs for l in lang2vocabs[lang].keys()]
            + list(string.digits)
            + list(string.punctuation)
        )

    def has_sufficient_valid_letters(
        self,
        title: str,
    ):
        num_valid_letters = len([t for t in title if t.lower() in self.vocab_letters])
        sufficient_valid_letters = (
            num_valid_letters / len(title) > self.lower_limit_proportion
        )
        return sufficient_valid_letters


unwanted = ["ja", "ar", "ko", "mn"]


def detect_is_known_lang(text: str):
    lang = just_try(lambda: lang_detect(text), default=None)
    is_good = is_good_lang(lang)
    return is_good


def is_good_lang(lang):
    if lang is not None:
        chinese = lang.startswith("zh")
        is_good = not chinese and lang not in unwanted
    else:
        is_good = False
    return is_good


@dataclass
class LangDetectedYoutubeResults(ContinuedCachedDicts):
    search_results_file: Union[_UNDEFINED, str] = UNDEFINED
    cache_base: PrefixSuffix = field(
        default_factory=lambda: BASE_PATHES["youtube_root"]
    )

    def generate_dicts_to_cache(self) -> Iterator[dict]:
        if os.path.isfile(self.jsonl_file):
            known_ids = [d["id"] for d in read_jsonl(self.jsonl_file)]
        else:
            known_ids = []
        print(f"already got {len(known_ids)} known_ids -> skipping these")
        g = tqdm(
            itertools.islice(
                read_jsonl(self.search_results_file),
                __start=len(known_ids),
                __stop=None,
            ),
            desc="reading results",
        )
        yield from (
            d | {"lang": just_try(lambda: lang_detect(d["title"]), default="no-lang")}
            for d in g
            # if d["id"] not in known_ids # simply skipping
        )


@dataclass
class GoodSearchResults(ContinuedCachedDicts):
    append_jsonl: ClassVar[str] = False
    all_results: Union[_UNDEFINED, LangDetectedYoutubeResults] = UNDEFINED

    def generate_dicts_to_cache(self) -> Iterator[dict]:
        all_results = list(self.all_results)
        good_results = list(
            filter(
                lambda d: is_good_lang(d["lang"]),
                tqdm(self.all_results, desc="filtering for good search results"),
            )
        )
        num_all_urls = len(all_results)
        print(f"all-urls: {num_all_urls}, good-lang {len(good_results)}")
        yield from good_results


if __name__ == "__main__":

    BASE_PATHES["youtube"] = f"/nm-raid/audio/work/thimmelsba/data/cache/YOUTUBE"

    GoodSearchResults(
        all_results=LangDetectedYoutubeResults(
            search_results_file=f"{BASE_PATHES['youtube_root']}/YOUTUBE_SEARCHING/results.jsonl"
        )
    )
    print(Counter(d["lang"] for d in read_jsonl(f"youtube_results_with_lang.jsonl")))
    # lang_detect_youtube_results()
    # known_langs = [v["lang"] for v in vocabs]
    # filta = ResultFilter(langs=known_langs).build()
    #
    # valid, invalid = [], []
    # for d in g:
    #     if is_known_lang(d["title"]):
    #         # if filta.has_sufficient_valid_letters(d["title"]):
    #         valid.append(d)
    #     else:
    #         invalid.append(d)
    #
    # write_jsonl(f"valid_youtube_results.jsonl", valid)
    # write_jsonl(f"invalid_youtube_results.jsonl", invalid)


"""
{
    "en": 811421,
    "de": 445715,
    "fr": 83827,
    "es": 15375,
    "it": 12915,
    "id": 10703,
    "nl": 10470,
    "ca": 10121,
    "pt": 8575,
    "af": 7903,
    "tr": 7448,
    "ru": 6711,
    "tl": 5578,
    "no": 5165,
    "ko": 4969,
    "ro": 4891,
    "sv": 4741,
    "da": 4469,
    "et": 4424,
    "vi": 4219,
    "pl": 3634,
    "so": 3257,
    "ar": 2480,
    "no-lang": 2327,
    "zh-cn": 2120,
    "fi": 1909,
    "sw": 1700,
    "hr": 1554,
    "sl": 1509,
    "hu": 1507,
    "ja": 1470,
    "cy": 1388,
    "bg": 1263,
    "cs": 834,
    "sk": 795,
    "lt": 790,
    "th": 761,
    "el": 526,
    "zh-tw": 520,
    "sq": 488,
    "fa": 456,
    "lv": 373,
    "uk": 347,
    "hi": 273,
    "bn": 262,
    "he": 191,
    "mk": 177,
    "ml": 128,
    "ta": 120,
    "pa": 62,
    "te": 54,
    "ur": 49,
    "ne": 39,
    "mr": 36,
    "kn": 11,
    "gu": 1,
}

"""
