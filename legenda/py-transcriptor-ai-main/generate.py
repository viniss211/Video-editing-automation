# -*- coding: utf-8 -*-

from textwrap import wrap
import numpy as np
from moviepy.editor import *
from moviepy.video.tools.subtitles import SubtitlesClip
from PIL import Image, ImageDraw, ImageFont
from pygemstones.util import log as l
import re
import codecs

# Função para converter o tempo SRT para segundos
def srt_time_to_seconds(srt_time):
    hours, minutes, seconds = srt_time.split(":")
    seconds, milliseconds = seconds.split(",")
    return int(hours) * 3600 + int(minutes) * 60 + int(seconds) + int(milliseconds) / 1000

# Função para ler o arquivo de transcrição no formato SRT
def read_transcript(file_path):
    with codecs.open(file_path, 'r', 'utf-8') as file:
        subtitles = []
        start_time, end_time, text = None, None, ""
        for line in file:
            line = line.strip()
            if re.match(r'^\d+$', line):
                if start_time is not None and end_time is not None:
                    subtitles.append(((start_time, end_time), text.strip()))
                start_time, end_time, text = None, None, ""
            elif re.match(r'\d{2}:\d{2}:\d{2},\d{3} --> \d{2}:\d{2}:\d{2},\d{3}', line):
                start_time_str, end_time_str = line.split(" --> ")
                start_time = srt_time_to_seconds(start_time_str.strip())
                end_time = srt_time_to_seconds(end_time_str.strip())
            elif line:
                text += (line + " ")
        if start_time is not None and end_time is not None:
            subtitles.append(((start_time, end_time), text.strip()))
    return subtitles

# Função geradora personalizada para criar as legendas
def generator(txt):
    wrapped_txt = "\n".join(wrap(txt, width=20))
    wrapped_txt = wrapped_txt.upper()

    img = Image.new("RGBA", (video.size[0], int(video.h * 0.2)), color=(0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    font = ImageFont.truetype(font_path, fontsize)

    left, top, right, bottom = d.multiline_textbbox((0, 0), wrapped_txt, font=font)
    text_width, text_height = right - left, bottom - top
    x = (img.width - text_width) // 2
    y = (img.height - text_height) // 2

    for i in range(-border_thickness, border_thickness + 1):
        for j in range(-border_thickness, border_thickness + 1):
            d.multiline_text(
                (x + i, y + j),
                wrapped_txt,
                font=font,
                fill=border_color,
                align="center",
            )

    d.multiline_text((x, y), wrapped_txt, font=font, fill="yellow", align="center")

    img_np = np.array(img)
    return ImageClip(img_np)

# Configuração inicial
l.d("Starting...")

# Carregar o vídeo original
video = VideoFileClip("temp/movie.mp4")
fontsize = int(video.h * 0.04)
font_path = "fonts/Montserrat-Black.ttf"
border_thickness = 8
border_color = "black"

# Ler o arquivo de transcrição com a codificação correta
l.d(f"Generating subtitles...")
subtitles_list = read_transcript("temp/transcript.txt")

# Criar o objeto de legendas utilizando a função geradora
subtitles = SubtitlesClip(subtitles_list, generator)

# Posicionar as legendas na parte inferior do vídeo
l.d(f"Setup subtitles...")
subtitles = subtitles.set_pos(("center", "bottom"))
subtitles = subtitles.set_start(0)
subtitles = subtitles.set_duration(video.duration)
subtitles = subtitles.margin(bottom=int(video.h * 0.12), opacity=0)

# Combinar as legendas com o vídeo original
l.d(f"Mixing video and subtitles...")
final_video = CompositeVideoClip([video, subtitles])

# Adicionar o áudio original ao vídeo
l.d(f"Adding original audio...")
final_video.audio = video.audio

# Exportar o vídeo final
l.d(f"Exporting final video...")
final_video.write_videofile(
    "temp/movie-out.mp4",
    fps=video.fps,
    codec="libx264",
    audio_codec="mp3",
)

l.s("Exported to temp/movie-out.mp4")
