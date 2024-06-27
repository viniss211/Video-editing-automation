from pygemstones.io import file as f
from pygemstones.system import runner as r
from pygemstones.util import log as l
import os
import codecs

os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

# setup
l.d("Starting...")

audio_file = "temp/audio.mp3"
transcript_file = "temp/transcript.txt"
whisper_transcript_file = "temp/transcript/audio.srt"
program = "whisper-ctranslate2"

# transcribe audio
l.d("Transcribing audio...")

r.run([
    program,
    "temp/audio.mp3",
    "--word_timestamps",
    "True",
    "--model",
    "medium",
    "--output_dir",
    "temp/transcript",
    "--max_line_width",
    "20",
    "--max_line_count",
    "2",
    "--suppress_tokens",
    "0,11,13,30",
])

# Ler arquivo de transcrição
with codecs.open(whisper_transcript_file, 'r', encoding='utf-8') as source_file:
    content = source_file.read()

# Escrever transcrição corrigida
with codecs.open(transcript_file, 'w', encoding='utf-8') as target_file:
    target_file.write(content)

l.s(f"Subtitles saved in {transcript_file} with UTF-8 encoding")
