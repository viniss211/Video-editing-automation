from moviepy.editor import VideoFileClip, AudioFileClip, CompositeAudioClip

# Carrega o vídeo e o áudio de fundo
video = VideoFileClip("video_editado.mp4")
background_audio = AudioFileClip("human.mp3")

# Reduz o volume do áudio de fundo
background_audio = background_audio.volumex(0.1)  # Ajuste o valor conforme necessário

# Define o áudio do vídeo original
original_audio = video.audio

# Cria um áudio composto com o áudio original do vídeo e o áudio de fundo
composite_audio = CompositeAudioClip([original_audio, background_audio.set_duration(video.duration)])

# Adiciona o áudio composto ao vídeo
final_video = video.set_audio(composite_audio)

# Salva o vídeo final
final_video.write_videofile("video_com_audio_de_fundo.mp4")
