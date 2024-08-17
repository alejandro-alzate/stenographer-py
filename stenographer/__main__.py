import time
import json
import os
start = time.time()
from values import LANGUAGES
import transcriber
import translator
import argparse

args = {}

# Defaults
flag_verbose = False
flag_filename = ""
flag_overwrite = False
flag_translation_list = ["es"]

flag_whisper_model = "medium"
flag_ollama_model = "llama3"

# print(args)
parser = argparse.ArgumentParser("Stenographer.py")
parser.add_argument("audio", help="Audio file to process")
parser.add_argument("-wm", "--whisper-model", default=flag_whisper_model, help="Model to use during the transcription process")
parser.add_argument("-om", "--ollama-model", default=flag_ollama_model, help="Model to use during the transcription process")
parser.add_argument("-tl", "--translation-list", default=json.dumps(flag_translation_list), help="\'[\"es \"]\' A list containing languages for translation.")
parser.add_argument("-ow", "--overwrite", default="True" if flag_overwrite else "False", help="[True / (False)] Overwrite files if they exist")
parser.add_argument("-v", "--verbose", default="True" if flag_verbose else "False", help="[True / (False)] Show extra information")

args = parser.parse_args()

# Parsing flags
flag_verbose = args.verbose == "True"
flag_filename = args.audio
flag_overwrite = args.overwrite == "True"
flag_translation_list = json.loads(args.translation_list)

flag_whisper_model = args.whisper_model
flag_ollama_model = args.ollama_model
if flag_verbose:
	print("Called with the following flags:")
	#This is what in lua would be a for k, v loop
	#Python "magic" as sublime likes to call it
	#Sure is something...
	for k in args.__dict__:
		v = args.__dict__[k]
		print(f"\t{k} = {v}")
	print()
def transcribe():
	transcriber.flag_verbose = flag_verbose
	transcriber.flag_filename = flag_filename
	transcriber.flag_overwrite = flag_overwrite
	transcriber.flag_whisper_model = flag_whisper_model
	transcriber.all()

def translate():
	translator.flag_verbose = flag_verbose
	translator.flag_overwrite = flag_overwrite
	translator.flag_ollama_model = flag_ollama_model
	for path in transcriber.write_jobs:
		if isinstance(flag_translation_list, list):
			for l in flag_translation_list:
				if l != transcriber.lang:
					translator.flag_language = l
					translator.translate(path)
				else:
					print(f"Skipping translation on {LANGUAGES[l]}, This is the detected source language.")
		elif isinstance(flag_translation_list, str):
			translator.flag_language = l
			translator.translate(path)

transcribe()
translate()

end = time.time()
print(f"[Finished in {end - start}]")