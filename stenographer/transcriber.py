import whisper
import os
#from whisper.utils import get_writer
from utils import get_writer
#from typing import Optional, Union

from codes import LANGUAGES

lang = False
audio = False
model = False
result = False
verbose = False
filename = False
overwrite = False
trim_audio = False
default_model_type = "medium"

default_word_options = {
	"highlight_words": True,
	"max_line_count": 2,
	"max_line_width": 20
}

def load_audio(path: str) -> list:
	global audio
	global filename
	filename = path
	print("JOB: Load audio.")
	if os.path.isfile(path):
		audio = whisper.pad_or_trim(whisper.load_audio(path)) if trim_audio else whisper.load_audio(path)
	else:
		print(f"\tThis is not a file: {path}")
	print("\tDone.")
	return audio

def load_model(model_type: str = default_model_type):
	global model
	model = whisper.load_model(model_type)
	return model

def detect_language() -> str:
	global lang
	print(f"JOB: Detect language.")

	if type(audio) == type(False):
		print("\tFirst load the audio.")
		return

	if type(model) == type(False):
		print("\tFirst load the model.")
		return

	mel = whisper.log_mel_spectrogram(whisper.pad_or_trim(audio)).to(model.device)
	options = whisper.DecodingOptions(fp16=False)
	_, probs = model.detect_language(mel)
	lang = max(probs, key=probs.get)

	print(f"\tDetected language: {LANGUAGES[lang]}")
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

	print(f"JOB: Language transcription in {LANGUAGES[lang]}")
	result = model.transcribe(audio, language=lang, fp16=False, verbose=verbose)

def write_result(customPath: str = os.path.dirname(filename or "./"), wordOptions: dict = default_word_options) -> bool:
	print("JOB: Write results.")

	if type(filename) == type(False):
		print("\tFirst load the audio.")
		return

	if type(result) == type(False):
		print("\tFirst transcribe the audio.")
		return

	if type(lang) == type(False):
		print("\tFirst detect language.")
		return

	name, ext = os.path.splitext(filename)
	srt_path = customPath
	srt_name = f"{name}.{lang}.srt"
	srt_filename = f"{srt_path}{srt_name}"

	proceed_flag = False
	if os.path.isfile(srt_path + srt_name):
		if overwrite:
			print("\tThis file already exist! Overwriting file as per the transcriber.overwrite directive.")
			proceed_flag = True

		else:
			print("\tThis file already exist! Avoiding overwrite as per the transcriber.overwrite directive.")
			proceed_flag = False
	else:
		proceed_flag = True

	if proceed_flag:
		print(f"\t--> {srt_filename}")
		# Modified writers now only care about an absolute path
		srt_writer = get_writer("srt")
		srt_writer(result, srt_filename, wordOptions)

	return proceed_flag

def all(audioPath: str, modelType: str = default_model_type, customPath: str = "./", customWordOptions: dict = default_word_options):
	load_audio(audioPath)
	load_model(modelType)
	detect_language()
	transcribe()
	write_result(customPath, customWordOptions)