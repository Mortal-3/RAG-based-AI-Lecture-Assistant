# Speech to Text
import whisper
import os
import json
model = whisper.load_model("large-v2")
for filename in os.listdir("audios"):
    if filename.endswith(".mp3"):
        print(f"Processing file: {filename}")
        result = model.transcribe(audio= f"audios/{filename}",
                                    langusage="hindi",
                                    task="transcribe",
                                    word_timestamps=False)
        # print(result["segments"])
        chunks=[]
        for segment in result["segments"]:
            print(f"Segment: {segment['text']}")
            chunks.append({"start": segment['start'], 'end': segment['end'], 'text': segment['text']})
        with open("output.json", "w") as f:
            json.dump(chunks, f) 