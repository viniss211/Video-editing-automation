import os
from dotenv import load_dotenv
import assemblyai as aai
from pygemstones.util import log as l

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()

# Configurar logging
l.d("Iniciando...")

# Obter chave da API do ambiente
api_key = os.getenv('API_KEY')

if api_key is None:
    raise EnvironmentError("A variável de ambiente API_KEY não está definida.")

# Configurar a chave da API para a AssemblyAI
aai.settings.api_key = api_key

subtitle_words = 5
audio_file = "temp/audio.mp3"
transcript_file = "temp/transcript.txt"
language_code = "pt-BR"  # Substituir pelo código de idioma correto

# Transcrever áudio
l.d("Transcrevendo áudio...")

config = aai.TranscriptionConfig(language_code=language_code)

transcriber = aai.Transcriber()

try:
    transcript = transcriber.transcribe(audio_file, config)
except Exception as e:
    l.e(f"Erro ao transcrever áudio: {str(e)}")
    raise

# Verificar se a transcrição retornou dados válidos
if transcript is None or not hasattr(transcript, 'words') or not isinstance(transcript.words, list):
    l.e("A transcrição não retornou dados válidos ou não possui uma lista de palavras.")
    if transcript is not None:
        l.e(f"Objeto de transcrição: {transcript}")
    raise ValueError("A transcrição não retornou dados válidos.")

# Formatar função de tempo
def format_time(milliseconds):
    seconds, milliseconds = divmod(milliseconds, 1000)
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    return f"{hours:02d}:{minutes:02d}:{seconds:02d},{milliseconds:03d}"

# Escrever legendas
try:
    with open(transcript_file, "w", encoding="utf-8") as file:
        l.d("Escrevendo legendas...")

        srt_string = ""
        subtitle_count = 1
        buffer = []

        # Inicializar tempo final anterior como 0
        previous_end_time = 0

        for word in transcript.words:
            text = word.text

            # Tempo de início é o mesmo que o tempo final anterior
            start_time = previous_end_time
            end_time = word.end

            buffer.append(text)

            if len(buffer) == subtitle_words:
                srt_string += f"{subtitle_count}\n"
                srt_string += f"{format_time(start_time)} --> {format_time(end_time)}\n"
                srt_string += " ".join(buffer) + "\n\n"

                subtitle_count += 1
                buffer = []

                # Atualizar tempo anterior para mantê-lo visível
                previous_end_time = end_time

        # Verificar se ainda há palavras no buffer
        if buffer:
            srt_string += f"{subtitle_count}\n"
            srt_string += f"{format_time(previous_end_time)} --> {format_time(end_time)}\n"
            srt_string += " ".join(buffer) + "\n\n"

        file.write(srt_string)

    l.s(f"Legendas salvas em {transcript_file}")

except Exception as e:
    l.e(f"Erro ao escrever legendas: {str(e)}")
    raise
