from fastapi import FastAPI, File, UploadFile
import whisper
import os

app = FastAPI()

model = None

@app.on_event("startup")
def load_model():
    global model
    model = whisper.load_model("base")

@app.get("/")
def root():
    return {"message": "API do Whisper está rodando!"}

@app.post("/transcribe/{language}")
async def transcribe(
    language: str,
    file: UploadFile = File(...)
):
    # Gera nome temporário para o arquivo recebido
    filename = f"temp_audio.{file.filename.split('.')[-1]}"
    with open(filename, "wb") as f:
        f.write(await file.read())

    # Faz a transcrição com o idioma definido na URL
    result = model.transcribe(filename, language=language)

    # Remove o arquivo temporário
    os.remove(filename)

    return {"text": result["text"]}
