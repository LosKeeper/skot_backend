import os
import json
from collections import defaultdict

def inspect_files(folder_path):
    audio_files = defaultdict(lambda: defaultdict(lambda: defaultdict(list)))
    for root, _, files in os.walk(folder_path):
        grandparent_dir = os.path.basename(os.path.dirname(root))  # Répertoire parent supplémentaire
        for file in files:
            if file.endswith((".aac", ".wav", ".flac")):
                file_path = os.path.join(root, file)
                file_info = {
                    "file_codec": os.path.splitext(file)[1].replace(".", ""),
                    "file_path": file_path.replace("\\", "/"),  # Utilisation des slashes vers le style Unix
                    "file_size": os.path.getsize(file_path)
                }
                parent_dir = os.path.basename(root)
                file_name_without_extension = os.path.splitext(file)[0]
                audio_files[grandparent_dir][parent_dir][file_name_without_extension].append(file_info)

    json_data = json.dumps(audio_files, indent=4)
    with open("audio/audio_files.json", "w") as json_file:
        json_file.write(json_data)