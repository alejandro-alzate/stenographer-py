#import whisper
import os
import gc
from utils import get_writer
from values import LANGUAGES, default_word_options
from stringsTranscriber import get_message

lang = False
audio = False
model = False
result = False
whisper = False

flag_fp16 = False
flag_verbose = False
flag_filename = False
flag_overwrite = False
flag_whisper_model = "large"
flag_language = "en"  # Default language

write_jobs = []
default_model_type = "medium"

def load_whisper():
	global whisper
	if (whisper is False) or (whisper is None):
		import whisper

def load_audio() -> list:
	global audio
	print(get_message(flag_language, "load_audio"))
	if os.path.isfile(flag_filename):
		load_whisper()
		audio = whisper.load_audio(flag_filename)
	else:
		print(get_message(flag_language, "file_not_found", filename=flag_filename))
		raise SystemError("File not found.")
	print("\tDone.\n")
	return audio

def load_model():
	print(get_message(flag_language, "load_model"))
	global model
	load_whisper()
	model = whisper.load_model(flag_whisper_model)
	print("\tDone.\n")
	return model

def detect_language() -> str:
	global lang
	print(get_message(flag_language, "detect_language"))

	if (audio is False) or (audio is None):
		print(get_message(flag_language, "first_load_audio"))
		return

	if (model is False) or (model is None):
		print(get_message(flag_language, "first_load_model"))
		return

	load_whisper()
	mel = whisper.log_mel_spectrogram(whisper.pad_or_trim(audio)).to(model.device)
	options = whisper.DecodingOptions(fp16=flag_fp16)
	_, probs = model.detect_language(mel)
	lang = max(probs, key=probs.get)

	print(get_message(flag_language, "language_detected", language=LANGUAGES.get(lang, lang)))
	return lang

def transcribe():
	global result

	if (audio is False) or (audio is None):
		print(get_message(flag_language, "first_load_audio"))
		return

	if (lang is False) or (lang is None):
		print(get_message(flag_language, "first_detect_language"))
		return

	if (model is False) or (model is None):
		print(get_message(flag_language, "first_load_model"))
		return

	print(get_message(flag_language, "transcription_job", language=LANGUAGES.get(lang, lang)))
	result = model.transcribe(audio, language=lang, fp16=flag_fp16, verbose=flag_verbose)

def write_result(customPath: str = os.path.dirname(flag_filename or "./"), wordOptions: dict = default_word_options) -> bool:
	print(get_message(flag_language, "write_results"))

	if (audio is False) or (audio is None):
		print(get_message(flag_language, "first_load_audio"))
		return

	if (result is False) or (result is None):
		print(get_message(flag_language, "transcription_not_done"))
		return

	if (lang is False) or (lang is None):
		print(get_message(flag_language, "first_detect_language"))
		return

	name, ext = os.path.splitext(flag_filename)
	srt_name = f"{name}.{lang}.srt"
	srt_filename = f"{srt_name}"
	srt_generic_filename = f"{name}.srt"

	proceed = False
	if os.path.isfile(srt_filename):
		if flag_overwrite:
			print(get_message(flag_language, "file_exists_overwrite"))
			proceed = True
		else:
			print(get_message(flag_language, "file_exists_avoid_overwrite"))
			proceed = False
	else:
		proceed = True

	if proceed:
		write_jobs.append(srt_filename)
		print(f"\t--> {srt_filename}")
		srt_writer = get_writer("srt")
		srt_writer(result, srt_filename, wordOptions)
		srt_writer(result, srt_generic_filename, wordOptions)
	return srt_filename

def shutdown():
	print(get_message(flag_language, "shutdown"))
	global model
	global audio
	global lang
	global result

	del lang
	del audio
	del model
	del result

	lang = False
	audio = False
	model = False
	result = False

	gc.collect()

def all():
	load_audio()
	load_model()
	detect_language()
	transcribe()
	write_result()
	shutdown()
