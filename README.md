# youtube-audio-data

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
user/phoenix | 32359 | 6
user/DeutscheWelleEspanol | 29342 | 15
user/NoticiasUnoColombia | 23830 | 0
c/TV5MONDEInfo | 23203 | 123
user/tv5monde | 21710 | 522
user/deutschewelle | 20441 | 246
c/aljazeeraenglish | 15690 | 163
user/bbcnews | 15061 | 82
user/tagesschau | 14879 | 205
user/Elespectadorcom | 14814 | 1649
user/france24 | 14737 | 2
user/deutschewellerussian | 11379 | 9
user/deutschewelleenglish | 8786 | 403
user/spiegeltv | 8087 | 238
c/bayerischerrundfunk | 7652 | 1136
c/BR24 | 7603 | 2503
user/BBC | 7589 | 554
user/ArchivoNoticiasUno | 6441 | 0
user/BBCRussian | 6096 | 100
c/CanalMyNews | 5662 | 6
user/hrfernsehen | 5085 | 1734
c/BBCMundo | 4260 | 474
c/extra3 | 3852 | 2337
c/derStandardat | 3817 | 659
user/ARD | 3417 | 533
user/SWR | 3131 | 391
c/ZDFheute | 3027 | 63
user/TEDtalksDirector | 2748 | 2673
user/meinMDRFernsehen | 2314 | 559
c/mdr | 2239 | 541
user/srfkultur | 1936 | 79
c/srf | 1787 | 57
c/ORFFanHD | 1699 | 0
user/TracksARTEde | 1578 | 34
user/VanityFairMagazine | 1546 | 334
user/voxdotcom | 1351 | 1239
c/KURIERatWeb | 1348 | 2
c/artede | 1294 | 9
user/WDRchannel | 1212 | 463
c/ZDFMAGAZINROYALE | 1173 | 88
c/srfdok | 1141 | 526
user/ndr | 988 | 849
c/NDRDoku | 980 | 831
c/france3na | 948 | 3
c/heuteshow | 942 | 8
channel/UCFoKXoDoExwtBWdSTCIdEVQ | 900 | 1
user/sfarchiv | 763 | 54
user/rbb | 741 | 192
c/DWDocumentary | 710 | 210
puls | 692 | 114
user/walulissiehtfern | 584 | 267
c/gouvernementfr | 552 | 180
c/TV5MONDEAfrique | 522 | 65
c/terra-x | 518 | 440
c/WDRDoku | 406 | 253
c/BrowserBallett | 388 | 346
c/LaPulla | 367 | 337
c/terraxleschundco | 316 | 272
c/ykollektiv | 300 | 296
c/MDRDOK | 285 | 122
c/MDRInvestigativ | 263 | 86
c/ZDF | 257 | 37
c/DieFrage | 254 | 208
c/DRUCKDieSerie | 244 | 161
c/ZDFbesseresser | 237 | 57
c/followmereports | 219 | 202
c/germania | 214 | 187
c/aufklo | 202 | 184
c/STRGF | 193 | 177
c/TEDEspanol | 124 | 91
c/redfishstream | 124 | 86
c/scobel | 111 | 2
c/37Grad | 60 | 16
c/DerFall | 31 | 30
c/FunkOfficial | 31 | 9
user/vicenews | 29 | 5
c/ZDFwiso | 28 | 12
c/frontal | 9 | 8

### workflow -> TODO
* automate the "cycle": 

0. start with some known youtube-channels as initial "seed"
1. scraping channels -> meta-data; 
2. searching youtube with titles from step 0 -> channels
3. goto step 1

#### more detailed
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

### running code
* my beartype dataclass hack
```shell
export BEARTYPE_DATACLASSES_BASEDIR=${PWD}

```