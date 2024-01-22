import json
from termcolor import colored


class MessageGenerator:
    def __init__(self, file_path, logger):
        self.file_path = file_path
        self.logger = logger

    def AddMessage(self, title, message):
        try:
            with open(self.file_path, "r") as json_file:
                data = json.load(json_file)
        except FileNotFoundError:
            data = []

        if data != []:
            last_msg_id = data[-1]["id"]
        else:
            last_msg_id = -1
        data.append(
            {"id": last_msg_id + 1, "title": title, "message": message})

        with open(self.file_path, "w") as json_file:
            json.dump(data, json_file)

        self.logger.info(colored(
            f"Le message {title} a été ajouté avec succès.", "green"))

    def AddArtistSelection(self, title_list):
        with open(self.file_path, "w") as json_file:
            json.dump([
                {"title": title_list[0]},
                {"title": title_list[1]}

            ], json_file)
