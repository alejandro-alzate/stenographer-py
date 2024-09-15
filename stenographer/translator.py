from values import LANGUAGES, PROMPT_TEMPLATE, DUMMY_SRT
import ollama
import os
import gc
from stringsTranslator import get_message

flag_verbose = False
flag_overwrite = False
flag_censor_words = False
flag_ollama_model = "llama3"
flag_language = "en"

#Download the model if it's not already available.
def download_model() -> bool:
	try:
		ollama.chat(flag_ollama_model)
		if flag_verbose:
			print(get_message(flag_language, "model_present", model=flag_ollama_model))
		return True

	except ollama.ResponseError as e:
		print("\tError:", e.error)
		if e.status_code == 404:
			if flag_verbose:
				print(get_message(flag_language, "model_absent", model=flag_ollama_model))
			return ollama.pull(flag_ollama_model)
		else:
			return False

def load_model() -> None:
	print(f"[\033[3;34mTranslator\033[0;0m] {get_message(flag_language, 'load_job')}")
	download_model()

def prepare_prompt(srt_data, language: str) -> str:
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

def get_source_path(path: str) -> str:
	source = False
	name, ext = os.path.splitext(path)
	
	generic_source = os.path.isfile(name + ".srt")
	english_source = os.path.isfile(name + ".en.srt")

	if generic_source:
		source = name + ".srt"
	elif english_source:
		source = name + ".en.srt"
	elif ext == ".srt":
		source = path
	else:
		source = False
		raise SystemError("File not found.")

	return source

def get_target_path(path: str, language: str) -> str:
	#Generate the target file path based on the original file path and language.
	name, ext = os.path.splitext(path)
	srt_name = f"{name}.{language}.srt"
	return srt_name

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

def translate(path: str, language: str) -> None:
	#Main function to handle the translation process based on the specified mode.
	print(get_message(flag_language, 'translate_job', language=LANGUAGES.get(language, language)))
	download_model()

	source = get_source_path(path)
	target = get_target_path(path, language)
	srt_data = read_srt_content(source)
	prompt = prepare_prompt(srt_data, language)

	if overwrite_check(target):
		result = ollama.generate(
			model = flag_ollama_model,
			prompt = prompt,
			stream = False
			)

		#Responses will always get trimmed this is the fix:
		#								↓
		content = result["response"] + "\n\n"
		with open(target, "w") as f:
			print(f"\t--> {target}")
			f.write(content)

		if flag_verbose:
			print(content)
		print("\n")


	else:
		print("\n" + get_message(flag_language, "avoid_overwrite") + "\n")



