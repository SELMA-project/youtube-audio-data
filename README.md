# youtube-audio-data
#### this repo is mirrored to: https://github.com/SELMA-project/youtube-audio-data.git

finding/filtering/getting audio data from youtube

### legal aspects
["YouTube has never sued anyone for downloading content."](https://www.makeuseof.com/tag/is-it-legal-to-download-youtube-videos/)

### current state
* scraped a small collection of youtube-channels for their meta-data (no audio, no videos)
#### number of videos/subtitles per channel
* number of videos per channel (somewhen around december 2021, january 2022)
  * counted are "info-jsons" downloaded by yt-dlp
  * list of channels is just a manual selection, there are way more (interesting ones) not yet scraped!

* number of manually created (hopefully by human) subtitles per channel
  * counts of `vtt`-files written by `--all-subs` arg of yt-dlp
  * seems `--all-subs` is not really downloading ALL subtitles, but just manually created one (excluding youtube-generated ones)
  * quality of subtitles completely upto the users/channels -> needs to be estimated somehow
  * TODO: this does not tell how many videos have subtitles, but simply counds vtt-files! happens quite often that single video got multiple vtt-files!!

channel_name | num_info_jsons | num_vtt_files
--- | --- | ---
user/TEDxTalks | 99997 | 23355
c/euronewsfr | 99996 | 11
user/france24 | 96538 | 18
c/aljazeeraenglish | 89403 | 430
user/noticiascaracol | 88614 | 20757
user/RTIOFFICIEL | 70117 | 1
c/france3na | 36840 | 24
user/phoenix | 35619 | 7
user/DeutscheWelleEspanol | 32025 | 23
user/deutschewelle | 29077 | 264
c/TV5MONDEInfo | 28069 | 142
user/deutschewelleenglish | 27844 | 469
user/NoticiasUnoColombia | 24937 | 4
user/tv5monde | 21775 | 529
user/tagesschau | 17038 | 508
user/bbcnews | 16283 | 84
user/Elespectadorcom | 16200 | 2058
user/deutschewellearabic | 14614 | 0
user/deutschewellerussian | 12510 | 11
user/BBC | 11473 | 654
user/spiegeltv | 9200 | 394
c/BR24 | 8805 | 2533
c/bayerischerrundfunk | 7534 | 1234
c/CanalMyNews | 6871 | 7
user/BBCRussian | 6534 | 102
user/ArchivoNoticiasUno | 6440 | 0
user/vicenews | 5895 | 1628
user/hrfernsehen | 5750 | 6226
c/BBCMundo | 4379 | 574
c/derStandardat | 4341 | 971
c/ZDFheute | 4128 | 214
c/extra3 | 4081 | 2576
user/TEDtalksDirector | 3998 | 98929
user/ARD | 3295 | 510
user/SWR | 3211 | 451
user/vice | 2977 | 3006
user/DeutscheWelleHindi | 2953 | 4
c/mdr | 2613 | 618
user/meinMDRFernsehen | 2613 | 618
user/VanityFairMagazine | 2498 | 415
c/KURIERatWeb | 2166 | 7
c/srf | 2052 | 68
c/ORFFanHD | 1970 | 0
channel/UC2KCI1AXQVx1_XJmykB7cHA (DW-arabic-youtube) | 1613 | 0
user/TracksARTEde | 1557 | 43
c/artede | 1552 | 17
user/voxdotcom | 1398 | 2818
user/DWBahasaIndonesia | 1311 | 4
user/dwbengali | 1299 | 0
c/ZDFMAGAZINROYALE | 1222 | 114
c/srfdok | 1219 | 590
c/dwurdu | 1208 | 0
user/WDRchannel | 1054 | 621
c/NDRDoku | 1052 | 917
user/ndr | 1052 | 917
c/heuteshow | 1016 | 8
channel/UCFoKXoDoExwtBWdSTCIdEVQ | 985 | 1
user/sfarchiv | 969 | 61
c/Wikitongues | 816 | 476
c/DWDocumentary | 769 | 322
c/gouvernementfr | 763 | 244
puls/ | 725 | 148
user/srfkultur | 710 | 82
user/rbb | 686 | 198
user/walulissiehtfern | 618 | 304
c/terra-x | 552 | 491
c/TV5MONDEAfrique | 543 | 65
channel/UCET6sWl4Xcu-U8Ka9PJPrwA (DW-documentary-arabic-youtube) | 508 | 0
c/WDRDoku | 448 | 305
c/BrowserBallett | 410 | 474
c/LaPulla | 386 | 352
c/terraxleschundco | 344 | 338
c/ykollektiv | 333 | 364
channel/UC5pFu_fzPSg7RiLSRpjwBgg (DW-pashto-youtube) | 326 | 0
c/MDRInvestigativ | 320 | 138
c/ZDFbesseresser | 300 | 57
c/DRUCKDieSerie | 298 | 220
c/DekhoSunoJano | 293 | 282
c/MDRDOK | 293 | 156
c/DieFrage | 288 | 249
c/ZDF | 256 | 49
c/followmereports | 251 | 234
c/germania | 239 | 219
c/aufklo | 230 | 212
c/STRGF | 221 | 212
c/KainaatAstronomyinUrdu | 183 | 97
c/TEDEspanol | 180 | 147
c/scobel | 137 | 4
channel/UCumGF1yJ1ZMnpueabAyXqrw | 121 | 0
c/37Grad | 108 | 36
c/FunkOfficial | 78 | 10
c/dwdochindi | 66 | 62
c/DerFall | 48 | 47
c/frontal | 44 | 37
c/ZDFwiso | 42 | 13


### 2 workflows
#### 1. scraping a youtube-channel to get `info.json`s
```json
{
  "id": "aEZ7XX0E1bE",
  "title": "Zwischen Indien und Pakistan – die Sikhs | DW Dokumentation",
  "formats": [
    {
  ... 
```
#### 2. searching youtube
1. searching to get search-results
2. filter results by their title and whatever meta-data
3. download `info.json` via `yt-dlp` in `batch-file`mode

* example search-`result-json`
```json
{
  "id": "BhgCB_F7BFQ",
  "thumbnails": [
    "https://i.ytimg.com/vi/BhgCB_F7BFQ/hq720.jpg?sqp=-oaymwEjCOgCEMoBSFryq4qpAxUIARUAAAAAGAElAADIQj0AgKJDeAE=&rs=AOn4CLDXVB6uVcfBJ5QrT5FyTv1AuNvVgQ",
    "https://i.ytimg.com/vi/BhgCB_F7BFQ/hq720.jpg?sqp=-oaymwEXCNAFEJQDSFryq4qpAwkIARUAAIhCGAE=&rs=AOn4CLB4MCOresAXttKZBZYIP0fKdELmEA"
  ],
  "title": "El Salvador: Kampf gegen den Klimawandel | Global Ideas",
  "long_desc": null,
  "channel": "DW Deutsch",
  "duration": "5:13",
  "views": "2.704 Aufrufe",
  "publish_time": "vor 2 Wochen",
  "url_suffix": "/watch?v=BhgCB_F7BFQ",
  "rank": 0
}

```
#### downloading audios
1. filter by transcripts (see `.vtt` file)
2. download audio via `yt-dlp` in `batch-file` -mode

#### bootstrapped approach

0. start with some known youtube-channels as initial "seed"
1. scraping channels -> meta-data; 
2. searching youtube with titles from step 1. -> channels
3. goto step 1

#### more detailed (please do not yet read it, its just confusing, I have to organize it more!!)
##### TODO: copypasting+refactoring the code!
1. [scraping channels](download_metadata_from_youtube_channels.py)
2. [searching youtube](searching_youtube_with_channels.py): getting search-results: by searching youtube with search-phrases
    ```shell
   example search result:
    {
      "id": "BhgCB_F7BFQ",
      "thumbnails": [
        "https://i.ytimg.com/vi/BhgCB_F7BFQ/hq720.jpg?sqp=-oaymwEjCOgCEMoBSFryq4qpAxUIARUAAAAAGAElAADIQj0AgKJDeAE=&rs=AOn4CLDXVB6uVcfBJ5QrT5FyTv1AuNvVgQ",
        "https://i.ytimg.com/vi/BhgCB_F7BFQ/hq720.jpg?sqp=-oaymwEXCNAFEJQDSFryq4qpAwkIARUAAIhCGAE=&rs=AOn4CLB4MCOresAXttKZBZYIP0fKdELmEA"
      ],
      "title": "El Salvador: Kampf gegen den Klimawandel | Global Ideas",
      "long_desc": null,
      "channel": "DW Deutsch",
      "duration": "5:13",
      "views": "2.704 Aufrufe",
      "publish_time": "vor 2 Wochen",
      "url_suffix": "/watch?v=BhgCB_F7BFQ",
      "rank": 0
    }
    ```
3. [scraping subtitles](download_via_yt_dlp_from_urls.py): filter for "good" results + scrape subtitles
   1. [filter_youtube_results](filter_youtube_results.py) for "good" results (by titles language), num likes etc not reliable? 
   2. scraping subtitles
      ```shell
       data/ASR_DATA/YOUTUBE_subtitles# ll |  head
          90464 Jan  5 02:11 $13,950,000 2019 DAMEN YACHT SUPPORT VESSEL 'PINK SHADOW' SuperYacht Toy Hauler Tour [7ymEzBrldlI].ar.vtt
          76773 Jan  5 02:11 $13,950,000 2019 DAMEN YACHT SUPPORT VESSEL 'PINK SHADOW' SuperYacht Toy Hauler Tour [7ymEzBrldlI].de.vtt
         102343 Jan  5 02:11 $13,950,000 2019 DAMEN YACHT SUPPORT VESSEL 'PINK SHADOW' SuperYacht Toy Hauler Tour [7ymEzBrldlI].el.vtt
          74109 Jan  5 02:11 $13,950,000 2019 DAMEN YACHT SUPPORT VESSEL 'PINK SHADOW' SuperYacht Toy Hauler Tour [7ymEzBrldlI].en-US.vtt
          76356 Jan  5 02:11 $13,950,000 2019 DAMEN YACHT SUPPORT VESSEL 'PINK SHADOW' SuperYacht Toy Hauler Tour [7ymEzBrldlI].es.vtt
          78790 Jan  5 02:11 $13,950,000 2019 DAMEN YACHT SUPPORT VESSEL 'PINK SHADOW' SuperYacht Toy Hauler Tour [7ymEzBrldlI].fr.vtt
          76907 Jan  5 02:11 $13,950,000 2019 DAMEN YACHT SUPPORT VESSEL 'PINK SHADOW' SuperYacht Toy Hauler Tour [7ymEzBrldlI].id.vtt
      ```
4. [getting new channels]()
   1. filter+sort potential channels by language + some heuristic quality (of subtitles) measures
5. goto 1.!

### some resources / links
* [youtube_search](https://github.com/joetats/youtube_search/blob/master/youtube_search/__init__.py) very simple
* [youtube-transcript-api](https://github.com/jdepoix/youtube-transcript-api)
* [youtube-search-python](https://github.com/alexmercerind/youtube-search-python) -> more complex, more needed features?
* [youtube-dl](https://github.com/ytdl-org/youtube-dl) -> outdated!! abandoned!! don't use anymore!
* [yt-dlp](https://github.com/yt-dlp/yt-dlp) -> use this one!
* [ard_spider](https://github.com/fabsrc/mediathek_scraper/blob/master/mediathek_scraper/spiders/ard_spider.py)
  * this is no youtube!

```shell
yt-dlp --write-sub --write-info-json --dateafter now-1year --download-archive downloadedarchive.txt -f ba https://www.youtube.com/user/ARD/featured
yt-dlp --write-sub --write-info-json --dateafter now-2year --max-downloads 50 --download-archive downloadedarchive.txt --extract-audio --audio-format mp3 -f ba https://www.daserste.de/unterhaltung/krimi/tatort/videos/index.html
```

### simply filtering by number of views does not work!!
* this video only had 1 view before I found it! even though its "good" content!
![sven_schulze](resources/sven_schulze.jpg)
