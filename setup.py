from setuptools import setup, find_packages

VERSION = "0.0.0"
DESCRIPTION = "Stenographer.py - a transcription tool for your content."
LONG_DESCRIPTION = "Stenographer.py is a somewhat automatized tool for videos and audio transcriptions using the power of ollama and whisper"
AUTHOR = "Alejandro Alzate Sánchez"
AUTHOR_EMAIL = "alejandro-alzate@github.com"
DEPENDENCIES = [
	"whisper", "ollama", "psutil", "os", "asyncio",
	"json", "platform", "subprocess", "re", "sys",
	"zlib", "aiofiles", "gc"#, "colorama"
	]

setup(
	#God dammit stenographer is taken
	name = "whisper-stenographer",
	version = VERSION,
	author = AUTHOR,
	author_email = AUTHOR_EMAIL,
	description = DESCRIPTION,
	long_description = LONG_DESCRIPTION,
	packages = find_packages(),
	install_requires = DEPENDENCIES,

	#Of course nowadays everyone puts this buzzword because,
	#they of course do so don't mind me if i do it as well.
	#--------------------------↓
	keywords = ["automation", "ai", "captioning"],
	classifiers = [
		"Development Status :: 3 - Alpha"
		,"Programming Language :: Python :: 3"

		# The PyPi documentation is a painful mess
		# So I'm not even bothering, luarocks wins
		# it by a land slide with it's simplicity.

		#,"Intended Audience :: Accessibility"
		#,"Operating System :: Linux :: Linux"
		#,"Operating System :: Microsoft :: Windows"
		#,"Operating System :: MacOS :: MacOS X"
	]
	)
