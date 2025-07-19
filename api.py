from fastapi import FastAPI, File, UploadFile
import whisper
import os

app = FastAPI()
model = None

@app.on_event("startup")
def load_model():
    global model
    model = whisper.load_model("base")

def is_transcription_bad(text):
    # Critério simples: muito curto, vazio ou contém token de erro
    if not text or len(text.strip()) < 5:
        return True
    if "<|unk|>" in text:
        return True
    return False

@app.post("/transcribe/smart")
async def smart_transcribe(file: UploadFile = File(...)):
    filename = f"temp_audio.{file.filename.split('.')[-1]}"
    with open(filename, "wb") as f:
        f.write(await file.read())

    # 1. Tenta autodetect
    result_auto = model.transcribe(filename)
    text_auto = result_auto["text"]

    # 2. Se ruim, tenta inglês
    if is_transcription_bad(text_auto):
        result_en = model.transcribe(filename, language="en")
        text_en = result_en["text"]

        # 3. Se inglês também for ruim, tenta português
        if is_transcription_bad(text_en):
            result_pt = model.transcribe(filename, language="pt")
            text_pt = result_pt["text"]

            if not is_transcription_bad(text_pt):
                transcricao = text_pt
                idioma = "pt"
            else:
                transcricao = text_auto
                idioma = "indefinido"
        else:
            transcricao = text_en
            idioma = "en"
    else:
        transcricao = text_auto
        idioma = result_auto.get("language", "auto")

    os.remove(filename)
    return {
        "text": transcricao,
        "idioma_final": idioma
    }
