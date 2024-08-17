import time
import os
start = time.time()
import transcriber
import translator
import argparse

args = {}

flag_verbose = False
flag_filename = ""
flag_overwrite = False

flag_whisper_model = "medium"
flag_ollama_model = "llama2-uncensored"

# print(args)
parser = argparse.ArgumentParser("Stenographer.py")
parser.add_argument("audio", help="Audio file to process")
parser.add_argument("-wm", "--whisper-model", default=flag_whisper_model, help="Model to use during the transcription process")
parser.add_argument("-om", "--ollama-model", default=flag_ollama_model, help="Model to use during the transcription process")
parser.add_argument("-ow", "--overwrite", default="True" if flag_overwrite else "False", help="[True / (False)] Overwrite files if they exist")
parser.add_argument("-v", "--verbose", default="True" if flag_verbose else "False", help="[True / (False)] Show extra information")

args = parser.parse_args()


flag_verbose = args.verbose == "True"
flag_filename = args.audio
flag_overwrite = args.overwrite == "True"

flag_whisper_model = args.whisper_model
flag_ollama_model = args.ollama_model
if flag_verbose:
	print("Called with the following flags:\n")
	#This is what in lua would be a for k, v loop
	#Python "magic" as sublime likes to call it
	#Sure is something...
	for k in args.__dict__:
		v = args.__dict__[k]
		print(f"\t{k} = {v}")
	print("\n")

transcriber.flag_verbose = flag_verbose
transcriber.flag_filename = flag_filename
transcriber.flag_overwrite = flag_overwrite
transcriber.flag_whisper_model = flag_whisper_model
transcriber.all()

translator.flag_verbose = flag_verbose
translator.flag_overwrite = flag_overwrite
translator.flag_ollama_model = flag_ollama_model
for path in transcriber.write_jobs:
	translator.translate(path)

end = time.time()
print(f"[Finished in {end - start}]")