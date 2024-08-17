from values import LANGUAGES
from values import PROMPT_TEMPLATE
from values import DUMMY_SRT
import os
import ollama

import asyncio
from ollama import AsyncClient

flag_language = "es"
flag_overwrite = True
flag_ollama_stream = True
flag_censor_words = False
flag_ollama_model = "llama3"
flag_ollama_async = False
flag_ollama_stream = True


def check_model():
	#Check if the model is available.
	try:
		ollama.chat(flag_ollama_model)
	except ollama.ResponseError as e:
		print("\tError: ", e.error)
		return e
	else:
		return True

def download_model():
	#Download the model if it's not already available.
	try:
		ollama.chat(flag_ollama_model)
		#print(f"\tModel {flag_ollama_model} is on the machine downloaded already.")
		return True
	except ollama.ResponseError as e:
		print("\tError:", e.error)
		if e.status_code == 404:
			print(f"\tModel {flag_ollama_model} is not on the machine downloaded already.")
			return ollama.pull(flag_ollama_model)
		else:
			return False

def load_model():
	#Load or download the model as needed.
	print("[Translator] JOB: Load / Check / Download model.")
	if not check_model():
		download_model()
	print("\tDone.\n")

def prepare_prompt(srt_data):
	#Prepare the prompt with given SRT data and flags.
	prompt = PROMPT_TEMPLATE.format(
		censor = "Censor any swear word with `[ ___ ]`." if flag_censor_words else "Do not censor any swear",
		language = LANGUAGES.get(flag_language, flag_language),
		content = srt_data
		)
	return prompt

def read_srt_content(path: str) -> str:
	#Read content from an SRT file or return dummy content if the file does not exist.
	srt_data = DUMMY_SRT
	if os.path.isfile(path):
		with open(path, "r") as f:
			srt_data = f.read()
	else:
		print(f"There's no such file {path}")
	return srt_data

def get_target_path(path: str) -> str:
	#Generate the target file path based on the original file path and language.
	srt_name_lang, ext = os.path.splitext(path)
	srt_name, lang = os.path.splitext(srt_name_lang)
	target = srt_name + "." + flag_language + ext
	return target

def overwrite_check(target: str) -> bool:
	#Check if the file exists and if overwriting is allowed.
	proceed = False
	if os.path.isfile(target):
		if flag_overwrite:
			print("\tThis file already exist! Overwriting file as per the translator.flag_overwrite directive.")
			proceed = True

		else:
			print("\tThis file already exist! Avoiding overwrite as per the translator.flag_overwrite directive.")
			proceed = False
	else:
		proceed = True
	return proceed

def static_write(result, target):
	#Write static (non-streamed) content to the file.
	#Adding a new line just to be safe in spec.
	if flag_verbose:
		print(result["message"]["content"])

	response = result["message"]["content"] + "\n\n"
	with open(target, "w") as f:
		print(f"\t--> {target}")
		f.write(response)
	print("\n")

def streamed_write(result, target):
	#Write streamed content to the file as it's given.
	with open(target, "w") as f:
		for chunk in result:
			content = chunk["message"]["content"]
			if flag_verbose:
				print(content, end="", flush=True)
			f.write(content)
			f.flush()

		#Adding a new line just to be safe in spec.
		f.write("\n\n")
		f.flush()


def translate(path: str):
	#Main function to handle the translation process based on the specified mode.
	print(f"[Translator] JOB: Translate to {LANGUAGES.get(flag_language, flag_language)}.")
	download_model()

	target = get_target_path(path)
	srt_data = read_srt_content(path)
	prompt = prepare_prompt(srt_data)

	if overwrite_check(target):
		result = ollama.generate(stream=flag_ollama_stream, model=flag_ollama_model, prompt=prompt)
		if flag_ollama_stream:
			streamed_write(result, target)
		else:
			static_write(result, target)
	else:
		print("\nTranslation not performed due to overwrite restriction.\n")
