from fastapi import FastAPI, File, UploadFile
import whisper
import os

model = whisper.load_model("base")
app = FastAPI()

@app.post("/transcribe")
async def transcribe(file: UploadFile = File(...)):
    filename = "temp_audio." + file.filename.split(".")[-1]
    with open(filename, "wb") as f:
        f.write(await file.read())

    result = model.transcribe(filename)
    os.remove(filename)
    return {"text": result["text"]}
