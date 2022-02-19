import os

from misc_utils.prefix_suffix import BASE_PATHES, PrefixSuffix

base_path = os.environ["BASE_PATH"]
BASE_PATHES["base_path"] = base_path
BASE_PATHES["youtube_root"] = PrefixSuffix("base_path", "data/ASR_DATA/YOUTUBE")
