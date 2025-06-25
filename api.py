from fastapi import FastAPI, File, UploadFile
import whisper
import os

# Inicializa o app FastAPI
app = FastAPI()

# Carrega o modelo dentro de uma função "startup"
model = None

@app.on_event("startup")
def load_model():
    global model
    model = whisper.load_model("base")

@app.get("/")
def root():
    return {"message": "API do Whisper está rodando!"}

@app.post("/transcribe")
async def transcribe(file: UploadFile = File(...)):
    filename = f"temp_audio.{file.filename.split('.')[-1]}"
    with open(filename, "wb") as f:
        f.write(await file.read())

    result = model.transcribe(filename)
    os.remove(filename)
    return {"text": result["text"]}
