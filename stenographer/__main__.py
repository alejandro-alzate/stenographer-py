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
# print(args)

transcriber.flag_verbose = flag_verbose
transcriber.flag_filename = flag_filename
transcriber.flag_overwrite = flag_overwrite
transcriber.flag_whisper_model = flag_whisper_model
transcriber.all()

translator.flag_verbose = flag_verbose
translator.flag_overwrite = flag_overwrite
for path in transcriber.write_jobs:
	translator.translate(path)

end = time.time()
print(f"[Finished in {end - start}]")