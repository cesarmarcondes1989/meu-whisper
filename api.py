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

            # Decide qual é a menos ruim (você pode sofisticar esse critério)
            if not is_transcription_bad(text_pt):
                transcricao = text_pt
                idioma = "pt"
            else:
                transcricao = text_auto  # ou text_en/text_pt, pode escolher pelo maior texto, etc.
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
