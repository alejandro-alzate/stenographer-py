from values import LANGUAGES
from values import PROMPT_TEMPLATE
from values import DUMMY_SRT
import os
import ollama

#import asyncio
#To do: paralell prompts
#from ollama import AsyncClient

flag_censor_words = False
flag_ollama_model = "llama3"
flag_language = "es"


def check_model():
	try:
		ollama.chat(flag_ollama_model)
	except ollama.ResponseError as e:
		print("\tError: ", e.error)
		return e
	else:
		return True

def download_model():
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
	print("JOB: Load / Check / Download model.")
	if not check_model():
		download_model()
	print("Done.\n")

def prepare_prompt():
	prompt = PROMPT_TEMPLATE.format(
		censor = "Censor any swear word with `[ ___ ]`." if flag_censor_words else "Do not censor any swear",
		language = LANGUAGES[flag_language] if flag_language in LANGUAGES else flag_language,
		content = srt_data 
		)
	return prompt

def read_srt_content(path: str) -> str:
	srt_data = DUMMY_SRT
	if os.path.isfile(path):
		with open(path, "r") as f:
			srt_data = f.read()
	else:
		print(f"There's no such file {path}")
	return srt_data

def get_target_path(path: str) -> str:
	srt_name_lang, ext = os.path.splitext(path)
	srt_name, lang = os.path.splitext(srt_name_lang)
	target = srt_name + "." + flag_language + ext
	return target

def overwrite_check(target: str) -> bool:
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

def translate(path: str):
	print(f"JOB: Translate to {LANGUAGES[l]}.")
	download_model()

	srt_data = read_srt_content(path)
	prompt = prepare_prompt()
	target = get_target_path(path)

	#print(srt_name_lang, ext, srt_name, lang, target)
	result = ollama.generate(model=flag_ollama_model, prompt=prompt)

	#Adding a new line just to be safe in spec.
	response = result["response"] + "\n"

	if overwrite_check(target):
		with open(target, "w") as f:
			print(f"\t--> {target}")
			f.write(response)
			f.close()
	print("\n")
