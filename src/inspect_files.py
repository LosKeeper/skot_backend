import os
import json
from collections import defaultdict


def generate_file_metadata(file_path):
    file_name = os.path.basename(file_path)

    title = input(f"Titre du fichier {file_name}: ")
    artist = input(f"Artiste du fichier {file_name}: ")
    album = input(f"Album du fichier {file_name}: ")
    date = input(f"Date de publication de {file_name} (format YYYY-MM-DD): ")

    json_metadata = {
        title: {
            "file_path": file_path.replace("\\", "/").split(".")[0],
            "cover_path": file_path.replace("\\", "/").replace(file_name, "cover.jpg"),
            "artist": artist,
            "album": album,
            "date": date
        }
    }

    with open(file_path.replace(".wav", ".json"), "w") as json_file:
        json.dump(json_metadata, json_file, indent=4)

    return json_metadata


def generate_all_metadata(folder_path):
    available_songs_json = defaultdict(dict)
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.endswith(".wav"):
                # Check for the existence of a metadata file in the json file
                json_file = file.replace(".wav", ".json")
                if json_file in files:
                    with open(os.path.join(root, json_file), "r") as json_metadata:
                        available_songs_json.update(
                            json.load(json_metadata))
                else:
                    available_songs_json.update(
                        generate_file_metadata(os.path.join(root, file)))

    with open(os.path.join(folder_path, "files.json"), "w") as available_songs:
        json.dump(available_songs_json, available_songs, indent=4)
