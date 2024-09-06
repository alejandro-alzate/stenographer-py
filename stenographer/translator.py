from values import LANGUAGES, PROMPT_TEMPLATE, DUMMY_SRT
import ollama
import os
from stringsTranslator import get_message

flag_verbose = False
flag_overwrite = False
flag_censor_words = False
flag_ollama_model = "llama3"

#Download the model if it's not already available.
def download_model():
	try:
		ollama.chat(flag_ollama_model)
		if flag_verbose:
			print(f"\tModel {flag_ollama_model} is on the machine downloaded already.")
		return True

	except ollama.ResponseError as e:
		print("\tError:", e.error)
		if e.status_code == 404:
			if flag_verbose:
				print(get_message(flag_language, "model_not_downloaded", model=flag_ollama_model))
			return ollama.pull(flag_ollama_model)
		else:
			return False

def load_model():
	print(f"[\033[3;34mTranslator\033[0;0m] {get_message(flag_language, 'load_job')}")
	download_model()

def prepare_prompt(srt_data, language: str):
	#Prepare the prompt with given SRT data and flags.
	prompt = PROMPT_TEMPLATE.format(
		censor = "Censor any swear word with `[ ___ ]`." if flag_censor_words else "Do not censor any swears",
		language = LANGUAGES.get(language, language),
		content = srt_data
		)
	return prompt

def read_srt_content(path: str) -> str:
	#Read content from an SRT file or return dummy content if the file does not exist.
	srt_data = DUMMY_SRT
	if os.path.isfile(path):
		with open(path, "r") as f:
			temp = f.read()
			srt_data = ""
			srt_data = temp
	else:
		print(get_message(flag_language, "file_not_found", path=path))
	return srt_data

def get_target_path(path: str, language: str) -> str:
	#Generate the target file path based on the original file path and language.
	srt_name_lang, ext = os.path.splitext(path)
	srt_name, lang = os.path.splitext(srt_name_lang)
	target = srt_name + "." + language + ext
	return target

def overwrite_check(target: str) -> bool:
	#Check if the file exists and if overwriting is allowed.
	proceed = False
	if os.path.isfile(target):
		if flag_overwrite:
			print(get_message(flag_language, "overwrite_exist"))
			print(f"\t--> {target}")
			proceed = True

		else:
			print(get_message(flag_language, "avoid_overwrite"))
			proceed = False
	else:
		proceed = True
	return proceed

def translate(path: str, language: str):
	#Main function to handle the translation process based on the specified mode.
	print(f"[\033[3;34mTranslator\033[0;0m] {get_message(flag_language, 'translate_job', language=LANGUAGES.get(language, language))}")
	download_model()

	target = get_target_path(path, language)
	srt_data = read_srt_content(path)
	prompt = prepare_prompt(srt_data, language)

	if overwrite_check(target):
		result = ollama.generate(
			model = flag_ollama_model,
			prompt = prompt,
			stream = True
			)
		content = ""
		for chunk in stream:
			#if isinstance(chunk["message"]["content"], str):
			if flag_verbose:
				print(chunk['message']['content'], end='', flush=True)
			content = content + chunk['message']['content']

	else:
		print("\n" + get_message(flag_language, "translation_not_performed") + "\n")



