from values import LANGUAGES, PROMPT_TEMPLATE, DUMMY_SRT
import os
import aiofiles
import asyncio
import ollama
from ollama import AsyncClient

flag_verbose = False
flag_overwrite = True
flag_censor_words = False
flag_ollama_model = "llama3"
flag_ollama_= False
flag_ollama_stream = True
flag_ollama_async = True


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
	print("[\033[3;34mTranslator\033[0;0m] JOB: Load / Check / Download model.")
	if not check_model():
		download_model()
	print("\tDone.\n")

def prepare_prompt(srt_data, language: str):
	#Prepare the prompt with given SRT data and flags.
	prompt = PROMPT_TEMPLATE.format(
		censor = "Censor any swear word with `[ ___ ]`." if flag_censor_words else "Do not censor any swear",
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
		print(f"There's no such file {path}")
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
			print("\tThis file already exist! Overwriting file as per the translator.flag_overwrite directive.")
			print(f"\t--> {target}")
			proceed = True

		else:
			print("\tThis file already exist! Avoiding overwrite as per the translator.flag_overwrite directive.")
			proceed = False
	else:
		proceed = True
	return proceed

def async_static_write(target, prompt):
	#Write static (non-streamed) content to the file.
	result = AsyncClient().generate(stream=False, model=flag_ollama_model, prompt=prompt)
	if flag_verbose:
		print(result)
		print(result["message"]["content"])

	#Adding a new line just to be safe in spec.
	response = result["message"]["content"] + "\n\n"
	with aiofiles.open(target, "w") as f:
		print(f"\t--> {target}")
		f.write(response)
	print("\n")

def async_streamed_write(target, prompt):
	#Write streamed content to the file as it's given.
	with aiofiles.open(target, "w") as f:
		for chunk in AsyncClient().generate(stream=True, model=flag_ollama_model, prompt=prompt):
			content = chunk["message"]["content"]
			if flag_verbose:
				print(content, end="", flush=True)
			f.write(content)
			f.flush()

		#Adding a new line just to be safe in spec.
		print(f"\t--> {target}")
		f.write("\n")
		f.flush()

def static_write(target, prompt):
	#Write static (non-streamed) content to the file.
	#Adding a new line just to be safe in spec.
	result = ollama.generate(stream=False, model=flag_ollama_model, prompt=prompt)
	content = ""
	try:
		content = result["message"]["content"]
	except Exception as e:
		print(e)

	if flag_verbose:
		print(result, content)

	response = result["message"]["content"] + "\n\n"
	with open(target, "w") as f:
		print(f"\t--> {target}")
		f.write(response)
	print("\n")

def streamed_write(target, prompt):
	result = ollama.generate(stream=True, model=flag_ollama_model, prompt=prompt)
	#Write streamed content to the file as it's given.
	with open(target, "w") as f:
		for chunk in result:
			content = ""
			print(chunk)
			if chunk["message"]:
				if chunk["message"]["content"]:
					content = chunk["message"]["content"]
			if flag_verbose:
				print(content, end="", flush=True)
			f.write(content)
			f.flush()

		#Adding a new line just to be safe in spec.
		f.write("\n\n")
		f.flush()

def translate(path: str, language: str):
	#Main function to handle the translation process based on the specified mode.
	print(f"[\033[3;34mTranslator\033[0;0m] JOB: Translate to {LANGUAGES.get(language, language)}.")
	download_model()

	target = get_target_path(path, language)
	srt_data = read_srt_content(path)
	prompt = prepare_prompt(srt_data, language)

	if overwrite_check(target):
		static_write(target, prompt)

	# Disabled while i wrap my head around async nonsense
	# 	if flag_ollama_async:
	# 		if flag_ollama_stream:
	# 			if flag_verbose: print("async_streamed_write")
	# 			async_streamed_write(target, prompt)
	# 		else:
	# 			if flag_verbose: print("async_static_write")
	# 			async_static_write(target, prompt)
	# 	else:
	# 		if flag_ollama_stream:
	# 			if flag_verbose: print("streamed_write")
	# 			streamed_write(target, prompt)
	# 		else:
	# 			if flag_verbose: print("static_write")
	# 			static_write(target, prompt)
				
	else:
		print("\nTranslation not performed due to overwrite restriction.\n")
