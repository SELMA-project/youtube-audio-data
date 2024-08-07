german_youtube = [
    "user/ARD",
    "c/ZDF",
    "c/ZDFheute",
    "c/ZDFbesseresser",
    "c/ZDFMAGAZINROYALE",
    "c/ZDFwiso",
    "c/heuteshow",
    "c/frontal",
    "c/37Grad",
    "c/terraxleschundco",
    "c/terra-x",
    "c/scobel",
    "user/WDRchannel",
    "c/WDRDoku",
    "c/bayerischerrundfunk",
    "c/BR24",
    "c/mdr",
    "c/MDRDOK",
    "c/MDRInvestigativ",
    "user/meinMDRFernsehen",
    "user/rbb",
    "c/NDRDoku",
    "user/ndr",
    "c/extra3",
    "c/ORFFanHD",
    "user/spiegeltv",
    "user/SWR",
    "c/BrowserBallett",
    "c/DieFrage",
    "c/STRGF",
    "c/germania",
    "c/ykollektiv",
    "puls",
    "c/followmereports",
    "c/FunkOfficial",
    "c/aufklo",
    "user/hrfernsehen",
    "c/artede",
    "c/srfdok",
    "c/srf",
    "user/srfkultur",
    "user/sfarchiv",
    "user/TracksARTEde",
    "user/tagesschau",
    "user/walulissiehtfern",
    "channel/UCFoKXoDoExwtBWdSTCIdEVQ",  # WeltSpiegel
    "c/DerFall",
    "user/phoenix",
    "user/deutschewelle",
    "c/derStandardat",
    "c/KURIERatWeb",
    "c/DRUCKDieSerie",
]
english_youtube = [
    # english
    "user/voxdotcom",  # what is vox?
    "user/deutschewelleenglish",
    "c/DWDocumentary",
    "user/TEDtalksDirector",
    "user/BBC",
    "user/bbcnews",
    "c/aljazeeraenglish",
    "user/vice",
    "user/vicenews",
    "c/redfishstream",
    "user/VanityFairMagazine",
]

spanish_youtube = [
    "user/DeutscheWelleEspanol",
    "c/TEDEspanol",
    "c/BBCMundo",
    "user/NoticiasUnoColombia",
    "user/ArchivoNoticiasUno",
    "c/LaPulla",
    "user/Elespectadorcom",
    "user/noticiascaracol",
]

french_youtube = [
    "user/france24",
    "c/france3na",
    "c/euronewsfr",
    "c/TV5MONDEInfo",
    "user/tv5monde",
    "c/TV5MONDEAfrique",
    "user/RTIOFFICIEL",
    "c/gouvernementfr",
]
"""
this is a very (german) biased collection! hopefully it can be expanded by (programmatically) exploring more channels!
"""

russian_youtube = ["user/deutschewellerussian", "user/BBCRussian", "user/rtrussian"]
urdu_youtube = ["c/KainaatAstronomyinUrdu", "c/dwurdu", "c/DekhoSunoJano"]
hindi_youtube = ["c/dwdochindi", "user/DeutscheWelleHindi"]
arabic_youtube = ["channel/UCET6sWl4Xcu-U8Ka9PJPrwA", "user/deutschewellearabic"]
misc_dw_channels = [
    "channel/UC2KCI1AXQVx1_XJmykB7cHA", # dw-arabic
    "user/dwbengali",
    "user/DWBahasaIndonesia",
    "channel/UCumGF1yJ1ZMnpueabAyXqrw",
    "channel/UC5pFu_fzPSg7RiLSRpjwBgg", # pashto
]

brazilian = ["c/CanalMyNews"]
mixed_youtube = ["user/TEDxTalks","c/Wikitongues"]
youtube_channels = (
    german_youtube
    + english_youtube
    + french_youtube
    + spanish_youtube
    + russian_youtube
    + urdu_youtube
    + hindi_youtube
    + arabic_youtube
    + misc_dw_channels
    + brazilian
    + mixed_youtube
)

CHANNEL2REABABLE={
    "channel/UC2KCI1AXQVx1_XJmykB7cHA":"DW-arabic-youtube",
    "channel/UCET6sWl4Xcu-U8Ka9PJPrwA":"DW-documentary-arabic-youtube",
    "channel/UC5pFu_fzPSg7RiLSRpjwBgg":"DW-pashto-youtube",
}