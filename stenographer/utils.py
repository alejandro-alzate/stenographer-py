import os
import platform
import psutil
import asyncio
from values import MEMORY_THRESHOLD, INCLUDE_SWAP_MEMORY
from values import PROGRAM_LANGUAGES as PL
import locale

def get_system_language():
	system_locale = locale.getdefaultlocale()[0]
	language_code = system_locale.split('_')[0]
	allowed_languages = PL
	return language_code if language_code in allowed_languages else "en"



def set_own_process_priority(priority):
	if platform.system() == "Windows":
		PRIORITY_CLASSES = {
			'IDLE': psutil.IDLE_PRIORITY_CLASS,
			'BELOW_NORMAL': psutil.BELOW_NORMAL_PRIORITY_CLASS,
			'NORMAL': psutil.NORMAL_PRIORITY_CLASS,
			'ABOVE_NORMAL': psutil.ABOVE_NORMAL_PRIORITY_CLASS,
			'HIGH': psutil.HIGH_PRIORITY_CLASS,
			'REALTIME': psutil.REALTIME_PRIORITY_CLASS
		}
	else:
		PRIORITY_CLASSES = {
			'IDLE': psutil.IOPRIO_CLASS_IDLE,
			'BELOW_NORMAL': psutil.IOPRIO_CLASS_BE,
			'NORMAL': psutil.IOPRIO_CLASS_NONE,
			'REALTIME': psutil.IOPRIO_CLASS_RT
			}

	if priority not in PRIORITY_CLASSES:
		raise ValueError(f"Invalid priority level. Choose from: {', '.join(PRIORITY_CLASSES.keys())}")

	p = psutil.Process(os.getpid())
	p.nice(PRIORITY_CLASSES[priority])

def set_priority_of_process_and_descendants(pid, priority):
	def set_priority(p):
		try:
			p.nice(priority)
		except psutil.AccessDenied:
			print(f"Access denied when setting priority for PID {p.pid}")

	def process_tree(p):
		# Recursively set priority for the process tree
		children = p.children(recursive=True)
		set_priority(p)
		for child in children:
			set_priority(child)
	
	# Define priority levels
	PRIORITY_CLASSES = {
		'IDLE': psutil.IDLE_PRIORITY_CLASS,
		'BELOW_NORMAL': psutil.BELOW_NORMAL_PRIORITY_CLASS,
		'NORMAL': psutil.NORMAL_PRIORITY_CLASS,
		'ABOVE_NORMAL': psutil.ABOVE_NORMAL_PRIORITY_CLASS,
		'HIGH': psutil.HIGH_PRIORITY_CLASS,
		'REALTIME': psutil.REALTIME_PRIORITY_CLASS
	}
	
	if priority not in PRIORITY_CLASSES:
		raise ValueError(f"Invalid priority level. Choose from: {', '.join(PRIORITY_CLASSES.keys())}")

	try:
		p = psutil.Process(pid)
		process_tree(p)
	except psutil.NoSuchProcess:
		print(f"No process found with PID {pid}")

async def get_memory_percentages():
	# Get virtual memory details (physical RAM and swap)
	virtual_memory = psutil.virtual_memory()
	swap_memory = psutil.swap_memory()

	# Calculate physical memory percentages
	total_physical = virtual_memory.total
	used_physical = virtual_memory.used
	percent_physical_used = (used_physical / total_physical) * 100

	# Calculate swap memory percentages
	total_swap = swap_memory.total
	used_swap = swap_memory.used
	percent_swap_used = (used_swap / total_swap) * 100

	# Calculate combined memory usage
	total_memory = total_physical + total_swap
	used_memory = used_physical + used_swap
	percent_combined_used = (used_memory / total_memory) * 100

	return percent_physical_used, percent_swap_used, percent_combined_used

async def is_memory_under_threshold():
	#Check if the memory usage is below the defined threshold.
	physical, swap, combined = await get_memory_percentages()
	if INCLUDE_SWAP_MEMORY:
		return combined < MEMORY_THRESHOLD
	else:
		return physical < MEMORY_THRESHOLD

async def memory_check():
	while not await is_memory_under_threshold():
		m = MEMORY_THRESHOLD
		p, s, c = await get_memory_percentages()
		print("[Utils] INFO: Memory usage is high (Threshold: {:.1f}%, Physical: {:.1f}%, Swap: {:.1f}%, Total: {:.1f}%), waiting to dispatch more jobs.".format(m, p, s, c), end="\r")
		await asyncio.sleep(5)


#Taken from whisper.utils modified file routines
"""
MIT License

Copyright (c) 2022 OpenAI

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import platform
import subprocess
import json
import os
import re
import sys
import zlib
from typing import Callable, Optional, TextIO

system_encoding = sys.getdefaultencoding()

if system_encoding != "utf-8":

	def make_safe(string):
		# replaces any character not representable using the system default encoding with an '?',
		# avoiding UnicodeEncodeError (https://github.com/openai/whisper/discussions/729).
		return string.encode(system_encoding, errors="replace").decode(system_encoding)

else:

	def make_safe(string):
		# utf-8 can encode any Unicode code point, so no need to do the round-trip encoding
		return string


def exact_div(x, y):
	assert x % y == 0
	return x // y


def str2bool(string):
	str2val = {"True": True, "False": False}
	if string in str2val:
		return str2val[string]
	else:
		raise ValueError(f"Expected one of {set(str2val.keys())}, got {string}")


def optional_int(string):
	return None if string == "None" else int(string)


def optional_float(string):
	return None if string == "None" else float(string)


def compression_ratio(text) -> float:
	text_bytes = text.encode("utf-8")
	return len(text_bytes) / len(zlib.compress(text_bytes))


def format_timestamp(
	seconds: float, always_include_hours: bool = False, decimal_marker: str = "."
):
	assert seconds >= 0, "non-negative timestamp expected"
	milliseconds = round(seconds * 1000.0)

	hours = milliseconds // 3_600_000
	milliseconds -= hours * 3_600_000

	minutes = milliseconds // 60_000
	milliseconds -= minutes * 60_000

	seconds = milliseconds // 1_000
	milliseconds -= seconds * 1_000

	hours_marker = f"{hours:02d}:" if always_include_hours or hours > 0 else ""
	return (
		f"{hours_marker}{minutes:02d}:{seconds:02d}{decimal_marker}{milliseconds:03d}"
	)


class ResultWriter:
	extension: str

	# Disabled this is handled in transcriber.py
	# This is a reversible change.
	# def __init__(self, output_dir: str):
	# 	self.output_dir = output_dir


	def __call__(
		self, result: dict, audio_path: str, options: Optional[dict] = None, **kwargs
	):
		# Disabled this is handled in transcriber.py
		# This is a reversible change.
		# audio_basename = os.path.basename(audio_path)
		# audio_basename = os.path.splitext(audio_basename)[0]
		# output_path = os.path.join(
		# 	self.output_dir, audio_basename + "." + self.extension
		# )
		output_path = audio_path
		#Removed I fixed the actual source of the bug
		#output_path = audio_path[1:] if audio_path[0] == "." else audio_path

		#print(f"Writing to {output_path}")
		if not os.path.isdir(os.path.split(output_path)[0]):
			print("Target directory seems missing")
			if platform.system() == "Linux":
				subprocess.run(["touch", output_path])
			elif platform.system() == "Darwin":
				subprocess.run(["touch", output_path])
			elif platform.system() == "Windows":
				subprocess.run(f"echo "" > {output_path}")
			else:
				print("The hell am I running on?")
				raise NotImplementedError

		with open(output_path, "w", encoding="utf-8") as f:
			self.write_result(result, file=f, options=options, **kwargs)

	def write_result(
		self, result: dict, file: TextIO, options: Optional[dict] = None, **kwargs
	):
		raise NotImplementedError


class WriteTXT(ResultWriter):
	extension: str = "txt"

	def write_result(
		self, result: dict, file: TextIO, options: Optional[dict] = None, **kwargs
	):
		for segment in result["segments"]:
			print(segment["text"].strip(), file=file, flush=True)


class SubtitlesWriter(ResultWriter):
	always_include_hours: bool
	decimal_marker: str

	def iterate_result(
		self,
		result: dict,
		options: Optional[dict] = None,
		*,
		max_line_width: Optional[int] = None,
		max_line_count: Optional[int] = None,
		highlight_words: bool = False,
		max_words_per_line: Optional[int] = None,
	):
		options = options or {}
		max_line_width = max_line_width or options.get("max_line_width")
		max_line_count = max_line_count or options.get("max_line_count")
		highlight_words = highlight_words or options.get("highlight_words", False)
		max_words_per_line = max_words_per_line or options.get("max_words_per_line")
		preserve_segments = max_line_count is None or max_line_width is None
		max_line_width = max_line_width or 1000
		max_words_per_line = max_words_per_line or 1000

		def iterate_subtitles():
			line_len = 0
			line_count = 1
			# the next subtitle to yield (a list of word timings with whitespace)
			subtitle: list[dict] = []
			last = result["segments"][0]["words"][0]["start"]
			for segment in result["segments"]:
				chunk_index = 0
				words_count = max_words_per_line
				while chunk_index < len(segment["words"]):
					remaining_words = len(segment["words"]) - chunk_index
					if max_words_per_line > len(segment["words"]) - chunk_index:
						words_count = remaining_words
					for i, original_timing in enumerate(
						segment["words"][chunk_index : chunk_index + words_count]
					):
						timing = original_timing.copy()
						long_pause = (
							not preserve_segments and timing["start"] - last > 3.0
						)
						has_room = line_len + len(timing["word"]) <= max_line_width
						seg_break = i == 0 and len(subtitle) > 0 and preserve_segments
						if (
							line_len > 0
							and has_room
							and not long_pause
							and not seg_break
						):
							# line continuation
							line_len += len(timing["word"])
						else:
							# new line
							timing["word"] = timing["word"].strip()
							if (
								len(subtitle) > 0
								and max_line_count is not None
								and (long_pause or line_count >= max_line_count)
								or seg_break
							):
								# subtitle break
								yield subtitle
								subtitle = []
								line_count = 1
							elif line_len > 0:
								# line break
								line_count += 1
								timing["word"] = "\n" + timing["word"]
							line_len = len(timing["word"].strip())
						subtitle.append(timing)
						last = timing["start"]
					chunk_index += max_words_per_line
			if len(subtitle) > 0:
				yield subtitle

		if len(result["segments"]) > 0 and "words" in result["segments"][0]:
			for subtitle in iterate_subtitles():
				subtitle_start = self.format_timestamp(subtitle[0]["start"])
				subtitle_end = self.format_timestamp(subtitle[-1]["end"])
				subtitle_text = "".join([word["word"] for word in subtitle])
				if highlight_words:
					last = subtitle_start
					all_words = [timing["word"] for timing in subtitle]
					for i, this_word in enumerate(subtitle):
						start = self.format_timestamp(this_word["start"])
						end = self.format_timestamp(this_word["end"])
						if last != start:
							yield last, start, subtitle_text

						yield start, end, "".join(
							[
								re.sub(r"^(\s*)(.*)$", r"\1<u>\2</u>", word)
								if j == i
								else word
								for j, word in enumerate(all_words)
							]
						)
						last = end
				else:
					yield subtitle_start, subtitle_end, subtitle_text
		else:
			for segment in result["segments"]:
				segment_start = self.format_timestamp(segment["start"])
				segment_end = self.format_timestamp(segment["end"])
				segment_text = segment["text"].strip().replace("-->", "->")
				yield segment_start, segment_end, segment_text

	def format_timestamp(self, seconds: float):
		return format_timestamp(
			seconds=seconds,
			always_include_hours=self.always_include_hours,
			decimal_marker=self.decimal_marker,
		)


class WriteVTT(SubtitlesWriter):
	extension: str = "vtt"
	always_include_hours: bool = False
	decimal_marker: str = "."

	def write_result(
		self, result: dict, file: TextIO, options: Optional[dict] = None, **kwargs
	):
		print("WEBVTT\n", file=file)
		for start, end, text in self.iterate_result(result, options, **kwargs):
			print(f"{start} --> {end}\n{text}\n", file=file, flush=True)


class WriteSRT(SubtitlesWriter):
	extension: str = "srt"
	always_include_hours: bool = True
	decimal_marker: str = ","

	def write_result(
		self, result: dict, file: TextIO, options: Optional[dict] = None, **kwargs
	):
		for i, (start, end, text) in enumerate(
			self.iterate_result(result, options, **kwargs), start=1
		):
			print(f"{i}\n{start} --> {end}\n{text}\n", file=file, flush=True)
			


class WriteTSV(ResultWriter):
	"""
	Write a transcript to a file in TSV (tab-separated values) format containing lines like:
	<start time in integer milliseconds>\t<end time in integer milliseconds>\t<transcript text>

	Using integer milliseconds as start and end times means there's no chance of interference from
	an environment setting a language encoding that causes the decimal in a floating point number
	to appear as a comma; also is faster and more efficient to parse & store, e.g., in C++.
	"""

	extension: str = "tsv"

	def write_result(
		self, result: dict, file: TextIO, options: Optional[dict] = None, **kwargs
	):
		print("start", "end", "text", sep="\t", file=file)
		for segment in result["segments"]:
			print(round(1000 * segment["start"]), file=file, end="\t")
			print(round(1000 * segment["end"]), file=file, end="\t")
			print(segment["text"].strip().replace("\t", " "), file=file, flush=True)


class WriteJSON(ResultWriter):
	extension: str = "json"

	def write_result(
		self, result: dict, file: TextIO, options: Optional[dict] = None, **kwargs
	):
		json.dump(result, file)


def get_writer(
	# Disabled this is handled in transcriber.py
	# This is a reversible change.
	output_format: str#, output_dir: str
) -> Callable[[dict, TextIO, dict], None]:
	writers = {
		"txt": WriteTXT,
		"vtt": WriteVTT,
		"srt": WriteSRT,
		"tsv": WriteTSV,
		"json": WriteJSON,
	}

	if output_format == "all":
		# Disabled this is handled in transcriber.py
		# This is a reversible change.
		# all_writers = [writer(output_dir) for writer in writers.values()]
		all_writers = [writer() for writer in writers.values()]

		def write_all(
			result: dict, file: TextIO, options: Optional[dict] = None, **kwargs
		):
			for writer in all_writers:
				writer(result, file, options, **kwargs)

		return write_all

	# Disabled this is handled in transcriber.py
	# This is a reversible change.
	#return writers[output_format](output_dir)
	return writers[output_format]()
