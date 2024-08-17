import time
import json
import os
#start = time.time()
from values import LANGUAGES
from values import MEMORY_THRESHOLD
import transcriber
import translator
import argparse
import asyncio

args = {}

# Defaults
flag_filename = ""
flag_verbose = False
flag_overwrite = False

flag_whisper_model = "medium"
flag_ollama_model = "llama3"
flag_ollama_stream = True
flag_ollama_async = False
flag_translation_list = ["es"]

# print(args)
parser = argparse.ArgumentParser("Stenographer.py")

# General
parser.add_argument("audio", help="Audio file to process")
parser.add_argument("-ow", "--overwrite", default="True" if flag_overwrite else "False", help="[True / (False)] Overwrite files if they exist.")
parser.add_argument("-v", "--verbose", default="True" if flag_verbose else "False", help="[True / (False)] Show extra information.")

#Transcriber
parser.add_argument("-wm", "--whisper-model", default=flag_whisper_model, help="Model to use during the transcription process.")

#Translator
parser.add_argument("-om", "--ollama-model", default=flag_ollama_model, help="Model to use during the transcription process.")
parser.add_argument("-os", "--ollama-stream", default="True" if flag_ollama_stream else "False", help="Stream the ollama output on translation.")
parser.add_argument("-tl", "--translation-list", default=json.dumps(flag_translation_list), help="A JSON list (eg: \'[\"es \"]\') containing languages for translation.")
parser.add_argument("-oa", "--ollama-async", default="True" if flag_ollama_async else "False", help="Make ollama operations asychronous.")

args = parser.parse_args()

# Parsing flags
flag_verbose = args.verbose == "True"
flag_filename = args.audio
flag_overwrite = args.overwrite == "True"

flag_whisper_model = args.whisper_model

flag_ollama_model = args.ollama_model
flag_ollama_async = args.ollama_async == "True"
flag_ollama_stream = args.ollama_stream == "True"
flag_translation_list = json.loads(args.translation_list)

if flag_verbose:
	print("[Main] INFO: Called with the following flags:")
	#This is what in lua would be a for k, v loop
	#Python "magic" as sublime likes to call it
	#Sure is something...
	for k in args.__dict__:
		v = args.__dict__[k]
		print(f"\t{k} = {v}")
	print()

async def async_translate_path(path, languages):
	#Asynchronously handle translation for a given path and list of languages.

	#Prepare flags
	translator.flag_verbose = flag_verbose
	translator.flag_overwrite = flag_overwrite
	translator.flag_ollama_model = flag_ollama_model
	translator.flag_ollama_stream = flag_ollama_stream

	for l in languages:
		if l != transcriber.lang:
			translator.flag_language = l
			await asyncio.to_thread(translator.translate, path)
		else:
			print(f"[Main] INFO: Skipping translation on {LANGUAGES[l]}, This is the detected source language.")

def is_memory_under_threshold():
	#Check if the memory usage is below the defined threshold.
	return psutil.virtual_memory().percent < MEMORY_THRESHOLD

async def main():
	#Main function to execute translations asynchronously with concurrent job dispatching.
	transcriber.flag_verbose = flag_verbose
	transcriber.flag_filename = flag_filename
	transcriber.flag_overwrite = flag_overwrite
	transcriber.flag_whisper_model = flag_whisper_model

	#The transcription is a dependency for translation.
	transcriber.all()

	paths = transcriber.write_jobs
	
	#If cannot detect the core count is assumed to be 1
	core_count = os.cpu_count() or 1

	# if isinstance(flag_translation_list, list):
	# 	#Create a batches of jobs based on the core count
	# 	batches = [paths[i:i + core_count] for i in range(0, len(paths), core_count)]

	# 	#Use asyncio.gather to run jobs concurrently
	# 	tasks = []
	# 	for batch in batches:
	# 		for path in batch:
	# 			tasks.append(async_translate_path(path, flag_translation_list))

	# 	await asyncio.gather(*tasks)
	# elif isinstance(flag_translation_list, str):
	# 	#handle the single translation case
	# 	tasks = [async_translate_path(path, [flag_translation_list]) for path in paths]
	# 	await asyncio.gather(*tasks)

if __name__ == "__main__":
	start = time.time()
	asyncio.run(main())
	end = time.time()
	print(f"[Main] INFO: [Finished in {end - start}]")

# def transcribe():
# 	transcriber.flag_verbose = flag_verbose
# 	transcriber.flag_filename = flag_filename
# 	transcriber.flag_overwrite = flag_overwrite
# 	transcriber.flag_whisper_model = flag_whisper_model
# 	transcriber.all()

# def translate():
# 	translator.flag_verbose = flag_verbose
# 	translator.flag_overwrite = flag_overwrite
# 	translator.flag_ollama_model = flag_ollama_model
# 	translator.flag_ollama_stream = flag_ollama_stream
# 	for path in transcriber.write_jobs:
# 		if isinstance(flag_translation_list, list):
# 			for l in flag_translation_list:
# 				#print(l)
# 				if l != transcriber.lang:
# 					translator.flag_language = l
# 					translator.translate(path)
# 				else:
# 					print(f"[Main] INFO: Skipping translation on {LANGUAGES[l]}, This is the detected source language.")
# 		elif isinstance(flag_translation_list, str):
# 			translator.flag_language = l
# 			translator.translate(path)

# transcribe()
# translate()

# end = time.time()
# print(f"[Main] INFO: [Finished in {end - start}]")