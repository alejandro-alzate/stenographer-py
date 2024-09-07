# strings translator

MESSAGES = {
	"en": {
		"start_processing": "[\x1b[3;34mTranslator\x1b[0;0m] \x1b[3;34;0mINFO\x1b[0;0m: Starting processing...",
		"finished": "[\x1b[3;34mTranslator\x1b[0;0m] \x1b[3;34;0mINFO\x1b[0;0m: [Finished in {elapsed_time}]",
		"called_with_flags": "[\x1b[3;34mTranslator\x1b[0;0m] \x1b[3;34;0mINFO\x1b[0;0m: Called with the following flags:",
		"translation_not_performed": "[\x1b[3;34mTranslator\x1b[0;0m] \x1b[3;34;0mINFO\x1b[0;0m: Skipping translation on {language}, This is the detected source language.",
		"overwrite_exist": "This file already exist! Overwriting file as per the translator.flag_overwrite directive.",
		"avoid_overwrite": "This file already exist! Avoiding Overwrite file as per the translator.flag_overwrite directive.",
		"translate_job": "[\x1b[3;34mTranslator\x1b[0;0m] Translating to {language}.",
		"model_present": "[\x1b[3;34mTranslator\x1b[0;0m] Model {model} is on the machine downloaded already.",
		"model_abssent": "[\x1b[3;34mTranslator\x1b[0;0m] Model {model} is not on the machine downloaded already."
	},
	"es": {
		"start_processing": "[\x1b[3;34mTraductor\x1b[0;0m] \x1b[3;34;0mINFO\x1b[0;0m: Comenzando el procesamiento...",
		"finished": "[\x1b[3;34mTraductor\x1b[0;0m] \x1b[3;34;0mINFO\x1b[0;0m: [Finalizado en {elapsed_time}]",
		"called_with_flags": "[\x1b[3;34mTraductor\x1b[0;0m] \x1b[3;34;0mINFO\x1b[0;0m: Llamado con las siguientes banderas:",
		"translation_not_performed": "[\x1b[3;34mTraductor\x1b[0;0m] \x1b[3;34;0mINFO\x1b[0;0m: Omitiendo la traducción en {language}, Este es el idioma detectado.",
		"overwrite_exist": "Este archivo ya existe sobreescribiendo por la directiva translator.flag_overwrite.",
		"avoid_overwrite": "",
		"translate_job": "[\x1b[3;34mTraductor\x1b[0;0m] Traduciendo a {language}.",
		"model_present": "[\x1b[3;34mTraductor\x1b[0;0m] Modelo {model} se encuentra descargado en la máquina.",
		"model_abssent": "[\x1b[3;34mTraductor\x1b[0;0m] Modelo {model} no se encuentra descargado en la máquina."
	}
}

#Fucking name colision drove me insane:
#				↓
def get_message(message_language: str, key: str, **kwargs) -> str:
	"""
	Retrieve the message for a given language and key, formatting it with the provided arguments.
	
	:param language: Language code ('en' or 'es')
	:param key: Key for the message
	:param kwargs: Arguments to format the message
	:return: Formatted message string
	"""
	lang_messages = MESSAGES.get(message_language, MESSAGES["en"])  # Default to English if language not found
	message = lang_messages.get(key, key)  # Default to key if message not found
	return message.format(**kwargs)