# string main

MESSAGES = {
	"en": {
		"start_processing": "[\x1b[3;32mMain\x1b[0;0m] \x1b[3;34;0mINFO\x1b[0;0m: Starting processing...",
		"finished": "[\x1b[3;32mMain\x1b[0;0m] \x1b[3;34;0mINFO\x1b[0;0m: [Finished in {elapsed_time}]",
		"called_with_flags": "[\x1b[3;32mMain\x1b[0;0m] \x1b[3;34;0mINFO\x1b[0;0m: Called with the following flags:",
		"skipping_translation": "[\x1b[3;32mMain\x1b[0;0m] \x1b[3;34;0mINFO\x1b[0;0m: Skipping translation on {language}, This is the detected source language."
	},
	"es": {
		"start_processing": "[\x1b[3;32mPrincipal\x1b[0;0m] \x1b[3;34;0mINFO\x1b[0;0m: Comenzando el procesamiento...",
		"finished": "[\x1b[3;32mPrincipal\x1b[0;0m] \x1b[3;34;0mINFO\x1b[0;0m: [Finalizado en {elapsed_time}]",
		"called_with_flags": "[\x1b[3;32mPrincipal\x1b[0;0m] \x1b[3;34;0mINFO\x1b[0;0m: Llamado con las siguientes banderas:",
		"skipping_translation": "[\x1b[3;32mPrincipal\x1b[0;0m] \x1b[3;34;0mINFO\x1b[0;0m: Omitiendo la traducción en {language}, Este es el idioma detectado."
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
