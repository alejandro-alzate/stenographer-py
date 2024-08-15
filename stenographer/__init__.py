import time
start = time.time()
import transcriber
import translator
import argparse


parser = argparse.ArgumentParser("Stenographer.py")
parser.add_argument("audio", help="Audio file to process")
parser.add_argument("-m", "--model", default="medium", help="Model to use during the process")
args = parser.parse_args()

filename = args.audio
model_type = args.model

transcriber.overwrite = True
transcriber.verbose = True
transcriber.load_audio(filename)
transcriber.load_model(model_type)
transcriber.detect_language()
transcriber.transcribe()
transcriber.write_result()

end = time.time()
print(f"[Finished in {end - start}]")