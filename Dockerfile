FROM python:3.10-slim

RUN apt-get update && apt-get install -y ffmpeg git && apt-get clean

# Usa cache e aumenta resiliência da instalação
RUN pip install --upgrade pip && \
    pip install git+https://github.com/openai/whisper.git --trusted-host pypi.org --trusted-host files.pythonhosted.org --timeout=60 --retries=5

RUN pip install fastapi uvicorn python-multipart

WORKDIR /app
COPY api.py /app/api.py

EXPOSE 7860

CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "7860", "--root-path", "/whisper"]
