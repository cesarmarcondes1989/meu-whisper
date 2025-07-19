from fastapi import FastAPI, File, UploadFile
import whisper
import os

app = FastAPI()
model = None

@app.on_event("startup")
def load_model():
    global model
    model = whisper.load_model("base")  # Troque para "medium" ou "large" se quiser mais precisão

def is_transcription_bad(text):
    # Simples: curto, vazio ou contém token de erro
    if not text or len(text.strip()) < 5:
        return True
    if "<|unk|>" in text:
        return True
    # Pode sofisticar: verificar se texto tem só "?" ou caracteres estranhos, etc.
    return False

@app.post("/transcribe/smart")
async def smart_transcribe(file: UploadFile = File(...)):
    filename = f"temp_audio.{file.filename.split('.')[-1]}"
    with open(filename, "wb") as f:
        f.write(await file.read())

    # 1. Tenta forçar inglês
    result_en = model.transcribe(filename, language="en", task="transcribe")
    text_en = result_en["text"]

    # 2. Se inglês ruim, tenta autodetect
    if is_transcription_bad(text_en):
        result_auto = model.transcribe(filename, task="transcribe")
        text_auto = result_auto["text"]
    else:
        result_auto = None
        text_auto = ""

    # 3. Se autodetect ruim, tenta português
    if result_auto and is_transcription_bad(text_auto):
        result_pt = model.transcribe(filename, language="pt", task="transcribe")
        text_pt = result_pt["text"]
    else:
        result_pt = None
        text_pt = ""

    # Decide a melhor transcrição
    transcricoes = [
        ("en", text_en),
        ("auto", text_auto),
        ("pt", text_pt)
    ]
    melhores = [(lang, txt) for lang, txt in transcricoes if txt and not is_transcription_bad(txt)]
    if melhores:
        # Pega a transcrição mais longa como melhor (pode mudar o critério)
        melhor = max(melhores, key=lambda x: len(x[1]))
        idioma, transcricao = melhor
    else:
        idioma, transcricao = "indefinido", text_en or text_auto or text_pt

    os.remove(filename)
    return {
        "text": transcricao,
        "idioma_final": idioma,
        "tentativas": {
            "en": text_en,
            "auto": text_auto,
            "pt": text_pt
        }
    }
