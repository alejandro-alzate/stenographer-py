#As for now you can pick only between es and en
#If one string is missing the program may chrash
#I don't have the fallback behavior of language.lua
#here so be careful.
app_lang = "es"
app_fallback_lang = "en"
default_word_options = {
	"highlight_words": True,
	"max_line_count": 2,
	"max_line_width": 20
}

#Probably the ban treat will be enough to avoid prompt injections bugs.
#I won't bother stopping people though is mostly a safeguard if an AI
#matter is on the text.

PROMPT_TEMPLATE = """Translate the content between on the code block into the specified target language, making sure to preserve the SRT format exactly.

**Instructions:**
1. **Extract** the text on the code block.
2. **Translate** the text of the code block into the target language.
3. **Preserve** the SRT format, including time codes and caption numbering.
4. **Do not** include the any additional comments about the task.
5. **Only** respond with the text on the code block.
6. **Apply** the following censorship: {censor}.
7. Respond **only** on plain text (Do not use a code block as response).

Being unable to follow the rules with lead to a permanent ban.

Target language: {language}

```
{content}
```
"""

#This is the amount of memory where the job dispatch process for translation will stop
#This is an obligatory tweak on window because of course they have to with that bloat
MEMORY_THRESHOLD = 50
INCLUDE_SWAP_MEMORY = True


#########################################
# Do not touch zone						#
#########################################
# Below values are not for user tweaks	#
#										#
# They're constants more than anything	#
# else...								#
#########################################

DUMMY_SRT = """1
00:00:00,000 --> 00:00:01,000


"""

LANGUAGES = {
	"en": "english",
	"zh": "chinese",
	"de": "german",
	"es": "spanish",
	"ru": "russian",
	"ko": "korean",
	"fr": "french",
	"ja": "japanese",
	"pt": "portuguese",
	"tr": "turkish",
	"pl": "polish",
	"ca": "catalan",
	"nl": "dutch",
	"ar": "arabic",
	"sv": "swedish",
	"it": "italian",
	"id": "indonesian",
	"hi": "hindi",
	"fi": "finnish",
	"vi": "vietnamese",
	"he": "hebrew",
	"uk": "ukrainian",
	"el": "greek",
	"ms": "malay",
	"cs": "czech",
	"ro": "romanian",
	"da": "danish",
	"hu": "hungarian",
	"ta": "tamil",
	"no": "norwegian",
	"th": "thai",
	"ur": "urdu",
	"hr": "croatian",
	"bg": "bulgarian",
	"lt": "lithuanian",
	"la": "latin",
	"mi": "maori",
	"ml": "malayalam",
	"cy": "welsh",
	"sk": "slovak",
	"te": "telugu",
	"fa": "persian",
	"lv": "latvian",
	"bn": "bengali",
	"sr": "serbian",
	"az": "azerbaijani",
	"sl": "slovenian",
	"kn": "kannada",
	"et": "estonian",
	"mk": "macedonian",
	"br": "breton",
	"eu": "basque",
	"is": "icelandic",
	"hy": "armenian",
	"ne": "nepali",
	"mn": "mongolian",
	"bs": "bosnian",
	"kk": "kazakh",
	"sq": "albanian",
	"sw": "swahili",
	"gl": "galician",
	"mr": "marathi",
	"pa": "punjabi",
	"si": "sinhala",
	"km": "khmer",
	"sn": "shona",
	"yo": "yoruba",
	"so": "somali",
	"af": "afrikaans",
	"oc": "occitan",
	"ka": "georgian",
	"be": "belarusian",
	"tg": "tajik",
	"sd": "sindhi",
	"gu": "gujarati",
	"am": "amharic",
	"yi": "yiddish",
	"lo": "lao",
	"uz": "uzbek",
	"fo": "faroese",
	"ht": "haitian creole",
	"ps": "pashto",
	"tk": "turkmen",
	"nn": "nynorsk",
	"mt": "maltese",
	"sa": "sanskrit",
	"lb": "luxembourgish",
	"my": "myanmar",
	"bo": "tibetan",
	"tl": "tagalog",
	"mg": "malagasy",
	"as": "assamese",
	"tt": "tatar",
	"haw": "hawaiian",
	"ln": "lingala",
	"ha": "hausa",
	"ba": "bashkir",
	"jw": "javanese",
	"su": "sundanese",
	"yue": "cantonese",
}