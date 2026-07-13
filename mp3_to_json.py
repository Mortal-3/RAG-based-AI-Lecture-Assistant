
import whisper
import os
import json
model = whisper.load_model("large-v2")
audios=os.listdir("audios")
for audio in audios:
    if ("_" in audio) and (audio.endswith(".mp3")):
        print(f"Processing file: {audio}")
        number = audio.split('_')[0]
        title = audio.split('_')[1][:-4]
        print(f"Tutorial Number: {number}, Title: {title}") 
        result = model.transcribe(audio= f"audios/{audio}",
                                    language="hi",
                                    task="transcribe",
                                    word_timestamps=False)
        chunks=[]
        for segment in result["segments"]:
            print(f"Segment: {segment['text']}")
            chunks.append({"number": number, "title": title, "start": segment['start'], 'end': segment['end'], 'text': segment['text']})
        chunks_with_metadata = {"chunks": chunks, "text": result["text"]}
        with open(f"jsons/{audio}.json", "w") as f:
            json.dump(chunks_with_metadata, f)
