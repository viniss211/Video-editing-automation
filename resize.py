import cv2
import os
from moviepy.editor import VideoFileClip, AudioFileClip

def resize_video(input_path, output_path, width=1080, height=1920):
    try:
        # Abre o vídeo de entrada
        cap = cv2.VideoCapture(input_path)
        # Verifica se o vídeo foi aberto corretamente
        if not cap.isOpened():
            print("Erro ao abrir o arquivo de vídeo")
            return

        # Obtém as propriedades do vídeo original
        fps = cap.get(cv2.CAP_PROP_FPS)
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        
        # Cria o objeto VideoWriter para salvar o vídeo redimensionado
        temp_video_path = "temp/temp_video.mp4"
        out = cv2.VideoWriter(temp_video_path, fourcc, fps, (width, height))

        while True:
            ret, frame = cap.read()
            if not ret:
                break
            
            # Redimensiona o frame
            resized_frame = cv2.resize(frame, (width, height))
            
            # Escreve o frame redimensionado no vídeo de saída
            out.write(resized_frame)

        # Libera os objetos
        cap.release()
        out.release()
        print(f"Vídeo redimensionado salvo temporariamente em: {temp_video_path}")

        # Usando moviepy para adicionar o áudio original ao vídeo redimensionado
        video_clip = VideoFileClip(temp_video_path)
        original_clip = VideoFileClip(input_path)
        audio_clip = original_clip.audio

        final_clip = video_clip.set_audio(audio_clip)
        final_clip.write_videofile(output_path, codec='libx264')

        print(f"Vídeo final com áudio salvo em: {output_path}")

    except Exception as e:
        print(f"Ocorreu um erro: {e}")

    finally:
        # Remove o vídeo temporário
        if os.path.exists(temp_video_path):
            os.remove(temp_video_path)
            print(f"Vídeo temporário removido: {temp_video_path}")

# Caminho do vídeo de entrada
input_video = "IN/original_movie.mp4"

# Caminho do vídeo de saída
output_video = "OUT/movie_resized.mp4"

# Chama a função para redimensionar o vídeo
resize_video(input_video, output_video)
