FROM python:3.10-slim

RUN apt-get update && apt-get install -y ffmpeg git && apt-get clean

# Corrige o erro de hash do torch
RUN pip install --upgrade pip && \
    pip install --no-cache-dir git+https://github.com/openai/whisper.git --trusted-host pypi.org --trusted-host files.pythonhosted.org

RUN pip install fastapi uvicorn python-multipart

WORKDIR /app
COPY api.py /app/api.py

EXPOSE 7860

CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "7860"]
