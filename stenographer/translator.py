from codes import LANGUAGES
import os
import ollama
#import asyncio
#To do: paralell prompts
#from ollama import AsyncClient

flag_censor_words = False
flag_ollama_model = "llama3"
flag_language = "es"

#Probably the ban treat will be enough to avoid prompt injections bugs.
#I won't bother stopping people though is mostly a safeguard if an AI
#matter is on the text.

PROMPT_TEMPLATE = """Translate the content between `[[START OF CONTENT]]` and `[[END OF CONTENT]]` into the specified target language, making sure to preserve the SRT format exactly.

**Instructions:**
1. **Extract** the text between the `[[START OF CONTENT]]` and `[[END OF CONTENT]]` tags.
2. **Translate** this text into the target language.
3. **Preserve** the SRT format, including time codes and caption numbering.
4. **Do not** include the content tags or any additional sentences not even comments.
5. **Only** respond with the text.
6. **Apply** the following censorship: {censor}.

Target language: {language}

[[START OF CONTENT]]
{content}
[[END OF CONTENT]]
"""

def check_model():
	try:
		ollama.chat(flag_ollama_model)
	except ollama.ResponseError as e:
		print("Error: ", e.error)
		return e
	else:
		return True

def download_model():
	try:
		ollama.chat(flag_ollama_model)
		#print(f"Model {flag_ollama_model} is on the machine downloaded already.")
		return True
	except ollama.ResponseError as e:
		print('Error:', e.error)
		if e.status_code == 404:
			print(f"Model {flag_ollama_model} is not on the machine downloaded already.")
			return ollama.pull(flag_ollama_model)
		else:
			return False

def load_model():
	if not check_model():
		download_model()

def translate(path):
	print("JOB: Translate")

	srt_data = "<EMPTY CONTENT>"
	if os.path.isfile(path):
		with open(path, "r") as f:
			srt_data = f.read()

	prompt = PROMPT_TEMPLATE.format(
		censor = "Censor any swear word with `[ ___ ]`." if flag_censor_words else "Do not censor any swear word.",
		language = LANGUAGES[flag_language] if flag_language in LANGUAGES else flag_language,
		content = srt_data 
		)

	srt_name_lang, ext = os.path.splitext(path)
	srt_name, lang = os.path.splitext(srt_name_lang)
	target = srt_name + "." + flag_language + "." + ext

	download_model()
	#print(srt_name_lang, ext, srt_name, lang, target)
	print(ollama.generate(model=flag_ollama_model, prompt=prompt)["response"])

#print(ollama.pull(flag_ollama_model)["status"])
#print(type(ollama.pull(flag_ollama_model)))
#print(ollama.ps())