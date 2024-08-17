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

PROMPT_TEMPLATE = """Translate the content between on the code block into the specified target language, making sure to preserve the SRT format exactly.

**Instructions:**
1. **Extract** the text on the code block.
2. **Translate** the text of the code block into the target language.
3. **Preserve** the SRT format, including time codes and caption numbering.
4. **Do not** include the any additional comments about the task.
5. **Only** respond with the text on the code block.
6. **Apply** the following censorship: {censor}.
7. Respond **only** on plain text (Do not use a code block as response).

Being unable to follow the rules with lead to a permanent ban.

Target language: {language}

```
{content}
```
"""

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
		#print(f"Model {flag_ollama_model} is on the machine downloaded already.")
		return True
	except ollama.ResponseError as e:
		print("\tError:", e.error)
		if e.status_code == 404:
			print(f"\tModel {flag_ollama_model} is not on the machine downloaded already.")
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
		censor = "Censor any swear word with `[ ___ ]`." if flag_censor_words else "Do not censor any swear",
		language = LANGUAGES[flag_language] if flag_language in LANGUAGES else flag_language,
		content = srt_data 
		)

	srt_name_lang, ext = os.path.splitext(path)
	srt_name, lang = os.path.splitext(srt_name_lang)
	target = srt_name + "." + flag_language + ext

	download_model()
	#print(srt_name_lang, ext, srt_name, lang, target)
	result = ollama.generate(model=flag_ollama_model, prompt=prompt)


	proceed = False
	if os.path.isfile(srt_filename):
		if flag_overwrite:
			print("\tThis file already exist! Overwriting file as per the translator.flag_overwrite directive.")
			proceed = True

		else:
			print("\tThis file already exist! Avoiding overwrite as per the translator.flag_overwrite directive.")
			proceed = False
	else:
		proceed = True

	response = result["response"]
	if proceed:
		with open(target, "w") as f:
			print(f"\t--> {target}")
			f.write(response)
			f.close()
