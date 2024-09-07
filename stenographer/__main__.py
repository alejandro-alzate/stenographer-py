import time
import json
import os
import argparse
from utils import memory_check, get_memory_percentages
from values import LANGUAGES, MEMORY_THRESHOLD, INCLUDE_SWAP_MEMORY
from stringsMain import get_message

args = {}

# Defaults
flag_filename = ""
flag_verbose = False
flag_overwrite = False
flag_whisper_model = "medium"
flag_ollama_model = "llama3"
flag_ollama_stream = True
flag_ollama_async = False
flag_translation_list = ["es", "pt", "ru"]
flag_language = "en"  # Default language

# Argument parsing
parser = argparse.ArgumentParser("Stenographer.py")

# General
parser.add_argument("audio", help="Audio file to process")
parser.add_argument("-ow", "--overwrite", default="True" if flag_overwrite else "False", help="[True / (False)] Overwrite files if they exist.")
parser.add_argument("-pl", "--program-language", default=flag_language, help="Sets the language of the program.")
parser.add_argument("-v", "--verbose", default="True" if flag_verbose else "False", help="[True / (False)] Show extra information.")

# Transcriber
parser.add_argument("-wm", "--whisper-model", default=flag_whisper_model, help="Model to use during the transcription process.")

# Translator
parser.add_argument("-om", "--ollama-model", default=flag_ollama_model, help="Model to use during the translation process.")
parser.add_argument("-tl", "--translation-list", default=json.dumps(flag_translation_list), help="A JSON list (eg: '[\"es\"]') containing languages for translation.")
parser.add_argument("-os", "--ollama-stream", default="True" if flag_ollama_stream else "False", help="Stream the ollama output on translation.")
parser.add_argument("-oa", "--ollama-async", default="True" if flag_ollama_async else "False", help="Make ollama operations asynchronous.")

args = parser.parse_args()

# Parsing flags
flag_verbose = args.verbose == "True"
flag_filename = args.audio
flag_overwrite = args.overwrite == "True"
flag_language = args.program_language

flag_whisper_model = args.whisper_model
flag_ollama_model = args.ollama_model
flag_ollama_async = args.ollama_async == "True"
flag_ollama_stream = args.ollama_stream == "True"
flag_translation_list = json.loads(args.translation_list)

if flag_verbose:
	print(get_message(flag_language, "called_with_flags"))
	for k in args.__dict__:
		v = args.__dict__[k]
		print(f"\t{k} = {v}")
	print()

# Import modules after argument parsing
import transcriber
import translator

def transcribe():
	transcriber.flag_verbose = flag_verbose
	transcriber.flag_filename = flag_filename
	transcriber.flag_overwrite = flag_overwrite
	transcriber.flag_whisper_model = flag_whisper_model
	transcriber.flag_language = flag_language
	transcriber.all()

def translate():
	translator.flag_verbose = flag_verbose
	translator.flag_overwrite = flag_overwrite
	translator.flag_ollama_model = flag_ollama_model
	translator.flag_ollama_stream = flag_ollama_stream
	translator.flag_language = flag_language
	flag_filename = args.audio
	if isinstance(flag_translation_list, list):
		for lang in flag_translation_list:
			translator.translate(flag_filename, lang)

	# for path in transcriber.write_jobs:
	# 	if isinstance(flag_translation_list, list):
	# 		for l in flag_translation_list:
	# 			print(l)
	# 			if l != transcriber.lang:
	# 				translator.flag_language = l
	# 				translator.translate(path)
	# 			else:
	# 				print(get_message(flag_language, "skipping_translation", language=LANGUAGES.get(l, l)))
	# 	elif isinstance(flag_translation_list, str):
	# 		translator.flag_language = l
	# 		translator.translate(path)

def main():
	start = time.time()
	print(get_message(flag_language, "start_processing"))

	#transcribe()
	translate()

	end = time.time()
	elapsed_time = end - start
	print(get_message(flag_language, "finished", elapsed_time=f"{elapsed_time:.2f}"))

if __name__ == "__main__":
	main()
