# *Stenographer.py*
A somewhat automatized tool for video transcriptions using the power of ollama and whisper.

## To do:
- [ ] Ollama translator
- [ ] Improve arguments
- [ ] Allow in-code import
- [ ] Asynchronous run

## Features
- Simplicity (This is a trend on my repos)
- Mostly system agnostic
- Can be invoked from terminal

## Flaws
- Concerning programming choices
- Coded by a python noob

## Getting started
1. 📡 Get a copy of srt.lua from the [Official Repository](https://github.com/alejandro-alzate/stenographer.py) or [From PyPi](https://pypi.org/project/whisper-stenographer/)(if you wanna a debian move on you)
2. 💾 Grab the stenographer folder and put it on your project.
3. ⚙ Use it to your project like this
	```bash
	python3 stenographer /path/to/media/content.mp4
	```
4. 💎 Profit.
It'll generate a `.srt` file on the same folder where the media is located, with the language appended.
`/home/mint/Videos/cool vid.mp4` → `/home/mint/Videos/cool vid.en.srt`

Here's an example:
(Forgive the quality it is 8.1MB out of the 10MB github allows, there's audio if you want to turn it on)
<video src="https://github.com/user-attachments/assets/60023607-3d5e-4af7-8eed-556bbb945a7d">

