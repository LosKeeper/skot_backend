import os
import json
from collections import defaultdict
from termcolor import colored


class MetadataGenerator:
    def __init__(self, folder_path, logger, save_file_name="available_songs.json"):
        self.folder_path = folder_path
        self.logger = logger
        self.save_file_name = save_file_name
        self.available_songs_json = defaultdict(dict)
        self.generate_all_metadata()

    def generate_all_metadata(self):
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
                            self.test_and_regenerate_metadata(data, file, root)
                    else:
                        self.logger.info(colored(
                            f"Metadata du fichier {file} non trouvé, veuillez entrer les informations manquantes.", "yellow"))
                        self.available_songs_json.update(
                            self.generate_file_metadata(os.path.join(root, file)))

        with open(os.path.join(self.folder_path, self.save_file_name), "w") as available_songs:
            json.dump(self.available_songs_json, available_songs, indent=4)

    def test_and_regenerate_metadata(self, data, file, root):
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
                    self.generate_file_metadata(os.path.join(root, file)))

    def generate_file_metadata(self, file_path):
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
