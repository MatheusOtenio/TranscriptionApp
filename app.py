from fastapi import FastAPI, HTTPException # type: ignore
from pydantic import BaseModel # type: ignore
import yt_dlp # type: ignore
import whisper # type: ignore
import subprocess
import os
import uuid
from fastapi.middleware.cors import CORSMiddleware # type: ignore
from fastapi.staticfiles import StaticFiles # type: ignore

app = FastAPI()

# Configuração do CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configuração do FFmpeg
ffmpeg_path = r"C:\ffmpeg\ffmpeg-7.1-essentials_build\bin"
os.environ["PATH"] = ffmpeg_path + os.pathsep + os.environ["PATH"]

# Configuração do diretório de saída
output_dir = os.path.join(os.getcwd(), "frontend", "data")
os.makedirs(output_dir, exist_ok=True)
app.mount("/data", StaticFiles(directory=output_dir), name="data")

class VideoRequest(BaseModel):
    url: str

def baixar_video(url: str) -> tuple:
    """Baixa o vídeo e retorna os caminhos do vídeo e áudio."""
    try:
        video_id = str(uuid.uuid4())[:8]
        video_path = os.path.join(output_dir, f"video_{video_id}.webm")
        
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': video_path,
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        
        return video_path, video_id
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao baixar vídeo: {str(e)}")

def extrair_audio(video_path: str) -> str:
    """Extrai o áudio do vídeo usando FFmpeg."""
    audio_path = video_path.replace(".webm", ".wav")
    try:
        subprocess.run([
            os.path.join(ffmpeg_path, "ffmpeg.exe"),
            "-i", video_path, "-vn", "-acodec", "pcm_s16le", "-ar", "44100", "-ac", "2", audio_path
        ], check=True)
        return audio_path
    except subprocess.CalledProcessError as e:
        raise HTTPException(status_code=500, detail=f"Erro ao extrair áudio: {str(e)}")

def transcrever_audio(audio_path: str) -> str:
    """Transcreve o áudio usando Whisper."""
    try:
        modelo = whisper.load_model("tiny")  # Pode testar "base" se necessário
        resultado = modelo.transcribe(audio_path)
        return resultado["text"]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro na transcrição: {str(e)}")

@app.post("/transcrever/")
async def transcrever_video(request: VideoRequest):
    """Recebe uma URL, baixa o vídeo, extrai o áudio e transcreve, depois apaga os arquivos."""
    try:
        video_path, video_id = baixar_video(request.url)
        audio_path = extrair_audio(video_path)
        transcricao = transcrever_audio(audio_path)

        # Apagar os arquivos após a transcrição
        try:
            os.remove(video_path)
            os.remove(audio_path)
        except Exception as e:
            print(f"Erro ao excluir arquivos: {e}")

        return {
            "transcricao": transcricao,
            "audio_url": f"/data/video_{video_id}.wav",
            "video_url": f"/data/video_{video_id}.webm"
        }
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))