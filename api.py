from fastapi import FastAPI, File, UploadFile
import whisper
import os

# Inicializa o app FastAPI
app = FastAPI()

# Carrega o modelo Whisper
model = whisper.load_model("base")

# Rota raiz (teste de status)
@app.get("/")
async def root():
    return {"message": "API do Whisper está rodando!"}

# Rota de transcrição de áudio
@app.post("/transcribe")
async def transcribe(file: UploadFile = File(...)):
    # Salva o arquivo temporariamente
    filename = f"temp_audio.{file.filename.split('.')[-1]}"
    with open(filename, "wb") as f:
        f.write(await file.read())

    # Executa a transcrição
    result = model.transcribe(filename)

    # Remove o arquivo temporário
    os.remove(filename)

    return {"text": result["text"]}
