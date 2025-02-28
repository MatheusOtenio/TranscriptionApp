# YouTube Video Transcription Project

Este projeto permite transcrever vídeos do YouTube através de um link, utilizando um backend em Python com FastAPI e um frontend em React/Vite para a interface.

## Funcionalidades

- **Backend (FastAPI):**
  - Recebe um link do YouTube.
  - Baixa o áudio do vídeo.
  - Realiza a transcrição usando a biblioteca `whisper` (OpenAI).
  - Retorna o texto transcrito.

- **Frontend (React/Vite):**
  - Interface intuitiva para inserção do link.
  - Exibe o status do processamento (carregamento, conclusão, erro).
  - Mostra a transcrição resultante.

## Pré-requisitos

- [Python 3.9+](https://www.python.org/downloads/)
- [Node.js](https://nodejs.org/) (para o frontend)
- [FFmpeg](https://ffmpeg.org/download.html) (instalação necessária para a biblioteca `whisper`)

## Instalação

1. Clone o repositório:
   ```bash
   git clone https://github.com/seu-usuario/transcricao-youtube.git
   cd transcricao-youtube

2. Backend:
# Crie e ative um ambiente virtual (recomendado)
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Instale as dependências
pip install -r requirements.txt

3. Frontend:
cd frontend
npm install
