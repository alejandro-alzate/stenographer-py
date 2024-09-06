MESSAGES = {
	"en": {
		"model_downloaded": "Model {model} is on the machine downloaded already.",
		"model_not_downloaded": "Model {model} is not on the machine downloaded already.",
		"file_not_found": "There's no such file {path}",
		"overwrite_exist": "This file already exists! Overwriting file as per the translator.flag_overwrite directive.",
		"avoid_overwrite": "This file already exists! Avoiding overwrite as per the translator.flag_overwrite directive.",
		"translate_job": "JOB: Translate to {language}.",
		"translation_not_performed": "Translation not performed due to overwrite restriction.",
		"load_job": "JOB: Load / Check / Download model.",
		"censor_words": "Censor any swear word with `[ ___ ]`.",
		"do_not_censor": "Do not censor any swears"
	},
	"es": {
		"model_downloaded": "El modelo {model} ya está descargado en la máquina.",
		"model_not_downloaded": "El modelo {model} no está descargado en la máquina.",
		"file_not_found": "No existe tal archivo {path}",
		"overwrite_exist": "¡Este archivo ya existe! Sobrescribiendo el archivo según la directiva translator.flag_overwrite.",
		"avoid_overwrite": "¡Este archivo ya existe! Evitando sobrescritura según la directiva translator.flag_overwrite.",
		"translate_job": "TRABAJO: Traducir a {language}.",
		"translation_not_performed": "Traducción no realizada debido a la restricción de sobrescritura.",
		"load_job": "TRABAJO: Cargar / Verificar / Descargar modelo.",
		"censor_words": "Censura cualquier palabra grosera con `[ ___ ]`.",
		"do_not_censor": "No censures palabras groseras"
	}
}

def get_message(language: str, key: str, **kwargs) -> str:
	"""
	Retrieve the message for a given language and key, formatting it with the provided arguments.
	
	:param language: Language code ('en' or 'es')
	:param key: Key for the message
	:param kwargs: Arguments to format the message
	:return: Formatted message string
	"""
	lang_messages = MESSAGES.get(language, MESSAGES["en"])  # Default to English if language not found
	message = lang_messages.get(key, key)  # Default to key if message not found
	return message.format(**kwargs)
