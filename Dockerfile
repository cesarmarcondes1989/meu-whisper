FROM python:3.10-slim

WORKDIR /app

RUN apt-get update && apt-get install -y ffmpeg git && apt-get clean

COPY . .

RUN pip install --no-cache-dir git+https://github.com/openai/whisper.git
RUN pip install fastapi uvicorn python-multipart

EXPOSE 7860

CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "7860"]

