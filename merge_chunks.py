import os
import json
import math

n = 5

for filename in os.listdir("jsons"):
    if filename.endswith(".json"):
        file_path = os.path.join("jsons", filename)

        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)

            new_chunks = []
            num_chunks = len(data.get("chunks", []))
            num_groups = math.ceil(num_chunks / n)

            for i in range(num_groups):
                start_idx = i * n
                end_idx = min((i + 1) * n, num_chunks)

                chunks_group = data["chunks"][start_idx:end_idx]

                new_chunks.append({
                    "number": data["chunks"][start_idx]["number"],
                    "title": chunks_group[0]["title"],
                    "start": chunks_group[0]["start"],
                    "end": chunks_group[-1]["end"],
                    "text": " ".join(c["text"] for c in chunks_group)
                })

            # save file without double .json
            os.makedirs("newjson", exist_ok=True)

            with open(os.path.join("newjson", filename), "w", encoding="utf-8") as json_file:
                json.dump(
                    {
                        "chunks": new_chunks,
                        "text": data["text"]
                    },
                    json_file,
                    indent=4
                )