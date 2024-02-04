import os
import json
from collections import defaultdict
from termcolor import colored


class MetadataGenerator:
    def __init__(self, folder_path, logger):
        self.folder_path = folder_path
        self.logger = logger
        self.available_songs_json = defaultdict(dict)
        self.available_albums_json = defaultdict(dict)
        self.generate_available_songs()
        self.generate_available_albums()

    def generate_available_albums(self):
        for keys, values in self.available_songs_json.items():
            if values["album"] not in self.available_albums_json:
                self.available_albums_json[values["album"]].update(
                    {"cover_path": values["cover_path"], "artist": values["artist"].split('&')[0], "date": values["date"]})

            if "songs" in self.available_albums_json[values["album"]]:
                self.available_albums_json[values["album"]]["songs"].append(
                    {keys: values["file_path"], "track": values["track"]})
            else:
                self.available_albums_json[values["album"]].update(
                    {"songs": [{keys: values["file_path"], "track": values["track"]}]})

            self.available_albums_json[values["album"]]["songs"].sort(
                key=lambda song: int(song["track"]))

        with open(os.path.join(self.folder_path, "available_albums.json"), "w") as available_albums:
            json.dump(self.available_albums_json, available_albums, indent=4)

        self.logger.info(colored(
            f"Le fichier available_albums.json a été généré avec succès.", "green"))

    def generate_available_songs(self):
        """
        Parcours le dossier spécifié dans la variable d'environnement FOLDER et génère le fichier JSON contenant les metadata de chaque fichier.
        """
        for root, _, files in os.walk(self.folder_path):
            for file in files:
                if file.endswith(".wav"):
                    json_file = file.replace(".wav", ".json")
                    if json_file in files:
                        self.logger.info(
                            colored(f"Metadata du fichier {file} trouvé.", "green"))
                        with open(os.path.join(root, json_file), "r") as json_metadata:
                            data = json_metadata.read()
                            self.test_and_regenerate_song_metadata(
                                data, file, root)
                    else:
                        self.logger.info(colored(
                            f"Metadata du fichier {file} non trouvé, veuillez entrer les informations manquantes.", "yellow"))
                        self.available_songs_json.update(
                            self.generate_song_metadata(os.path.join(root, file)))

        with open(os.path.join(self.folder_path, "available_songs.json"), "w") as available_songs:
            json.dump(self.available_songs_json, available_songs, indent=4)

        self.logger.info(colored(
            f"Le fichier available_songs.json a été généré avec succès.", "green"))

    def test_and_regenerate_song_metadata(self, data, file, root):
        """ Teste si les metadata du fichier sont conformes et, si ce n'est pas le cas, génère les informations manquantes.

        Args:
            data (JSON): Les metadata du fichier.
            file (str): Le nom du fichier.
            root (str): Le chemin du dossier contenant le fichier.
        """
        expected_keys = ["file_path", "cover_path",
                         "artist", "album", "date", "track"]
        json_data = json.loads(data)
        for _, value in json_data.items():
            inner_keys = value.keys()
            if all(k in inner_keys for k in expected_keys):
                self.logger.info(
                    colored(f"Les metadata de {file} sont conformes.", "green"))
                self.available_songs_json.update(json_data)
            else:
                self.logger.info(colored(
                    f"Les metadata de {file} sont corrompus, veuillez entrer les informations manquantes.", "red"))
                self.available_songs_json.update(
                    self.generate_song_metadata(os.path.join(root, file)))

    def generate_song_metadata(self, file_path):
        """ Génère les metadata d'un fichier.

        Args:
            file_path (str): Le chemin du fichier.

        Returns:
            JSON: Les metadata du fichier.
        """
        file_name = os.path.basename(file_path)

        title = input(f"Titre du fichier {file_name}: ")
        artist = input(f"Artiste du fichier {file_name}: ")
        album = input(f"Album du fichier {file_name}: ")
        track = input(f"Numéro de piste du fichier {file_name}: ")
        date = input(
            f"Date de publication de {file_name} (format YYYY-MM-DD): ")

        json_metadata = {
            title: {
                "file_path": file_path.replace("\\", "/").split(".")[0],
                "cover_path": file_path.replace("\\", "/").replace(file_name, "cover.jpg"),
                "artist": artist,
                "album": album,
                "date": date,
                "track": track
            }
        }

        with open(file_path.replace(".wav", ".json"), "w") as json_file:
            json.dump(json_metadata, json_file, indent=4)

        return json_metadata
