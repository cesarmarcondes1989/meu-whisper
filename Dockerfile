FROM python:3.10-slim

# Instala dependências do sistema
RUN apt-get update && apt-get install -y ffmpeg git && apt-get clean

# Instala Whisper diretamente do GitHub
RUN pip install --upgrade pip && \
    pip install git+https://github.com/openai/whisper.git --trusted-host pypi.org --trusted-host files.pythonhosted.org --timeout=60 --retries=5

# Instala FastAPI e Uvicorn
RUN pip install fastapi uvicorn python-multipart

# Define a pasta de trabalho
WORKDIR /app

# Copia o código para dentro do container
COPY api.py /app/api.py

# Expõe a porta da API
EXPOSE 7860

# Comando para rodar o servidor
CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "7860"]
