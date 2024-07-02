from moviepy.editor import VideoFileClip, concatenate_videoclips, CompositeVideoClip
from moviepy.video.fx.all import fadein, fadeout
from pydub import AudioSegment
from pydub.silence import split_on_silence
import os

# Variáveis para definir o trecho inicial e final do vídeo desejado
start_cut = 0  # Tempo de início do corte em segundos
end_cut = 60   # Tempo de fim do corte em segundos

# Carregue o vídeo
video = VideoFileClip("movie-out.mp4")

# Certifique-se de que os tempos de corte não ultrapassem a duração do vídeo
if end_cut > video.duration:
    end_cut = video.duration

# Extraia o áudio do vídeo e salve como arquivo temporário
audio_tempfile = "temp_audio.wav"
video.audio.write_audiofile(audio_tempfile, fps=44100)

# Carregue o áudio com pydub
audio = AudioSegment.from_wav(audio_tempfile)

# Ajustar parâmetros de silêncio
min_silence_len = 1100  # Ajuste para capturar pausas naturais
# Ajuste para capturar pausas sem ser muito sensível aos ruídos de fundo
silence_thresh = -30

# Divida o áudio onde o silêncio é determinado pelos parâmetros ajustados
print("Dividindo o áudio em segmentos...")
chunks = split_on_silence(
    audio, min_silence_len=min_silence_len, silence_thresh=silence_thresh)
print(f"Total de segmentos de áudio encontrados: {len(chunks)}")

# Lista para armazenar os clipes de vídeo
video_clips = []

# Inicialize variáveis para controle de continuidade da fala
previous_end = 0

# Duração do efeito de transição (em segundos)
transition_duration = 0.7

# Percorra os chunks de áudio para determinar os tempos de início e fim
for i, chunk in enumerate(chunks):
    # Calcule a duração do chunk em segundos
    chunk_duration = len(chunk) / 1000.0

    # Determine o tempo de início e fim do chunk
    start_time = previous_end
    end_time = start_time + chunk_duration

    # Atualize o tempo de início para o próximo chunk
    previous_end = end_time + (min_silence_len / 1000.0)

    # Verifique se o tempo de início do corte está dentro deste chunk
    if start_time >= start_cut and start_time < end_cut:
        # Certifique-se de que os tempos não ultrapassem o tempo de fim do corte
        if end_time > end_cut:
            end_time = end_cut

        # Crie um subclipe do vídeo original sem a pausa
        video_clip = video.subclip(start_time, end_time)

        # Adicione efeitos de fade in e fade out para uma transição suave
        video_clip = fadein(video_clip, transition_duration).fx(
            fadeout, transition_duration)
        video_clips.append(video_clip)

# Verifique se a lista de clipes não está vazia
if video_clips:
    # Concatene todos os clipes de vídeo para formar o vídeo final com transições suaves
    final_video = concatenate_videoclips(video_clips, method="compose")

    # Exporte o vídeo final
    final_video.write_videofile(
        "video_editado.mp4", codec='libx264', fps=video.fps)

    print("Vídeo editado exportado com sucesso.")

else:
    print("Nenhum clipe de vídeo foi gerado. Verifique os parâmetros de divisão de silêncio.")

# Limpeza do arquivo temporário de áudio
os.remove(audio_tempfile)
