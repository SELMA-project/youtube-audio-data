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
c/euronewsfr | 96320 | 11
user/TEDxTalks | 89834 | 15981
user/noticiascaracol | 71437 | 11609
user/RTIOFFICIEL | 66054 | 1
user/rtrussian | 40478 | 152
user/phoenix | 32916 | 7
user/DeutscheWelleEspanol | 29342 | 15
user/NoticiasUnoColombia | 23830 | 0
c/TV5MONDEInfo | 23203 | 123
user/tv5monde | 21710 | 522
user/deutschewelle | 20441 | 246
c/aljazeeraenglish | 15690 | 163
user/tagesschau | 15359 | 205
user/bbcnews | 15061 | 82
user/Elespectadorcom | 14814 | 1649
user/france24 | 14737 | 2
user/deutschewellerussian | 11379 | 9
user/deutschewelleenglish | 8786 | 403
user/spiegeltv | 8267 | 285
c/BR24 | 8146 | 2512
c/bayerischerrundfunk | 7916 | 1198
user/BBC | 7589 | 554
user/ArchivoNoticiasUno | 6441 | 0
user/BBCRussian | 6096 | 100
c/CanalMyNews | 5662 | 6
user/hrfernsehen | 5308 | 2740
c/BBCMundo | 4260 | 474
c/extra3 | 3927 | 2413
c/derStandardat | 3817 | 659
user/ARD | 3442 | 551
c/ZDFheute | 3418 | 67
user/SWR | 3294 | 481
user/TEDtalksDirector | 2748 | 2673
c/mdr | 2478 | 655
user/meinMDRFernsehen | 2469 | 629
user/srfkultur | 1961 | 87
c/ORFFanHD | 1800 | 0
c/srf | 1789 | 58
user/TracksARTEde | 1593 | 35
user/VanityFairMagazine | 1546 | 334
c/artede | 1437 | 12
user/voxdotcom | 1351 | 1239
c/KURIERatWeb | 1348 | 2
user/WDRchannel | 1300 | 547
c/ZDFMAGAZINROYALE | 1183 | 89
c/srfdok | 1166 | 551
c/NDRDoku | 1066 | 908
user/ndr | 1048 | 902
c/heuteshow | 961 | 8
c/france3na | 948 | 3
channel/UCFoKXoDoExwtBWdSTCIdEVQ | 922 | 1
user/rbb | 835 | 227
user/sfarchiv | 771 | 54
c/DWDocumentary | 710 | 210
puls | 704 | 126
user/walulissiehtfern | 585 | 269
c/gouvernementfr | 552 | 180
c/terra-x | 529 | 452
c/TV5MONDEAfrique | 522 | 65
c/WDRDoku | 429 | 276
c/BrowserBallett | 402 | 363
c/LaPulla | 367 | 337
c/terraxleschundco | 324 | 280
c/MDRDOK | 315 | 150
c/ykollektiv | 313 | 313
c/MDRInvestigativ | 290 | 107
c/ZDF | 268 | 37
c/DieFrage | 266 | 222
c/ZDFbesseresser | 253 | 58
c/DRUCKDieSerie | 244 | 161
c/followmereports | 230 | 214
c/germania | 226 | 194
c/aufklo | 209 | 192
c/STRGF | 202 | 184
c/TEDEspanol | 124 | 91
c/redfishstream | 124 | 86
c/scobel | 119 | 2
c/37Grad | 69 | 18
c/DerFall | 36 | 35
c/ZDFwiso | 36 | 12
c/FunkOfficial | 35 | 9
user/vicenews | 29 | 5
c/frontal | 16 | 16

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
