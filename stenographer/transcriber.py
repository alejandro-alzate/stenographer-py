import whisper
import os
#from whisper.utils import get_writer
from utils import get_writer
#from typing import Optional, Union

from values import LANGUAGES

lang = False
audio = False
model = False
result = False

flag_fp16 = False
flag_verbose = False
flag_filename = False
flag_overwrite = False
flag_whisper_model = "medium"

write_jobs = []
default_model_type = "medium"

default_word_options = {
	"highlight_words": True,
	"max_line_count": 2,
	"max_line_width": 20
}

def load_audio() -> list:
	global audio
	print("[Transcriber] JOB: Load audio.")
	if os.path.isfile(flag_filename):
		audio = whisper.load_audio(flag_filename)
	else:
		print(f"\tThis is not a file: {flag_filename}")
	print("\tDone.\n")
	return audio

def load_model():
	print(f"[Transcriber] JOB: Load model.")
	global model
	model = whisper.load_model(flag_whisper_model)
	print("\tDone.\n")
	return model

def detect_language() -> str:
	global lang
	print(f"[Transcriber] JOB: Detect language.")

	if type(audio) == type(False):
		print("\tFirst load the audio.")
		return

	if type(model) == type(False):
		print("\tFirst load the model.")
		return

	mel = whisper.log_mel_spectrogram(whisper.pad_or_trim(audio)).to(model.device)
	options = whisper.DecodingOptions(fp16=flag_fp16)
	_, probs = model.detect_language(mel)
	lang = max(probs, key=probs.get)

	print(f"\tDetected language: {LANGUAGES[lang] if lang in LANGUAGES else lang}.")
	return lang

def transcribe():
	global result
	if type(audio) == type(False):
		print("\tFirst load the audio.")
		print(audio)
		return

	if type(lang) == type(False):
		print("\tFirst detect language.")
		return

	if type(model) == type(False):
		print("\tFirst load the model.")
		return

	print(f"[Transcriber] JOB: Language transcription in {LANGUAGES[lang] if lang in LANGUAGES else lang}")
	print("\n")
	result = model.transcribe(audio, language=lang, fp16=flag_fp16, verbose=flag_verbose)
	print("\n")

def write_result(customPath: str = os.path.dirname(flag_filename or "./"), wordOptions: dict = default_word_options) -> bool:
	print("[Transcriber] JOB: Write results.")

	if type(flag_filename) == type(False):
		print("\tFirst load the audio.")
		return

	if type(result) == type(False):
		print("\tFirst transcribe the audio.")
		return

	if type(lang) == type(False):
		print("\tFirst detect language.")
		return

	name, ext = os.path.splitext(flag_filename)
	srt_name = f"{name}.{lang}.srt"
	srt_filename = f"{srt_name}"

	proceed = False
	if os.path.isfile(srt_filename):
		if flag_overwrite:
			print("\tThis file already exist! Overwriting file as per the transcriber.flag_overwrite directive.")
			proceed = True

		else:
			print("\tThis file already exist! Avoiding overwrite as per the transcriber.flag_overwrite directive.")
			proceed = False
	else:
		proceed = True

	if proceed:
		write_jobs.append(srt_filename)
		print(f"\t--> {srt_filename}")
		# Modified writers now only care about an absolute path
		srt_writer = get_writer("srt")
		srt_writer(result, srt_filename, wordOptions)
	return srt_filename

def all():
	load_audio()
	load_model()
	detect_language()
	transcribe()
	write_result()