# string transcriber

MESSAGES = {
	"en": {
		"load_audio": "[\033[3;35mTranscriber\033[0;0m] JOB: Load audio.",
		"file_not_found": "\tThis is not a file: {filename}",
		"load_model": "[\033[3;35mTranscriber\033[0;0m] JOB: Load model.",
		"detect_language": "[\033[3;35mTranscriber\033[0;0m] JOB: Detect language.",
		"first_load_audio": "\tFirst load the audio.",
		"first_load_model": "\tFirst load the model.",
		"first_detect_language": "\tFirst detect language.",
		"transcription_job": "[\033[3;35mTranscriber\033[0;0m] JOB: Language transcription in {language}",
		"write_results": "[\033[3;35mTranscriber\033[0;0m] JOB: Write results.",
		"file_exists_overwrite": "\tThis file already exists! Overwriting file as per the transcriber.flag_overwrite directive.",
		"file_exists_avoid_overwrite": "\tThis file already exists! Avoiding overwrite as per the transcriber.flag_overwrite directive.",
		"transcription_not_done": "\tFirst transcribe the audio.",
		"shutdown": "[\033[3;35mTranscriber\033[0;0m] JOB: \"De-allocate\" memory.",
		"language_detected": "Detected language: {language}.\n"
	},
	"es": {
		"load_audio": "[\033[3;35mTranscriptor\033[0;0m] TRABAJO: Cargar audio.",
		"file_not_found": "\tEsto no es un archivo: {filename}",
		"load_model": "[\033[3;35mTranscriptor\033[0;0m] TRABAJO: Cargar modelo.",
		"detect_language": "[\033[3;35mTranscriptor\033[0;0m] TRABAJO: Detectar idioma.",
		"first_load_audio": "\tPrimero carga el audio.",
		"first_load_model": "\tPrimero carga el modelo.",
		"first_detect_language": "\tPrimero detecta el idioma.",
		"transcription_job": "[\033[3;35mTranscriptor\033[0;0m] TRABAJO: Transcripción de idioma en {language}",
		"write_results": "[\033[3;35mTranscriptor\033[0;0m] TRABAJO: Escribir resultados.",
		"file_exists_overwrite": "\t¡Este archivo ya existe! Sobrescribiendo el archivo según la directiva transcriber.flag_overwrite.",
		"file_exists_avoid_overwrite": "\t¡Este archivo ya existe! Evitando sobrescritura según la directiva transcriber.flag_overwrite.",
		"transcription_not_done": "\tPrimero transcribe el audio.",
		"shutdown": "[\033[3;35mTranscriptor\033[0;0m] TRABAJO: \"Liberar\" memoria.",
		"language_detected": "Idioma detectado: {language}.\n"
	}
}

#Fixed before it caused mayhem
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
