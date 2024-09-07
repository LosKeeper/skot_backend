import re
import datetime as dt
import json


class NginxParser:
    def __init__(self, nginx_access_file_path, json_available_songs_path):
        self.dict = {}
        self.parse(nginx_access_file_path, json_available_songs_path)

    def parse(self, nginx_access_file_path, json_available_songs_path):
        with open(json_available_songs_path, 'r') as file:
            metadata_dict = json.load(file)

        with open(nginx_access_file_path, 'r') as file:
            lines = file.readlines()
            for line in lines:
                if line.startswith('#'):
                    continue
                match = re.search(
                    r'\[(.*?)\].*?"GET (/audio/[^/]+/[^/]+/[^/]+\.(wav|aac|flac))', line)
                if match:
                    date_str = match.group(1)
                    date_formated = dt.datetime.strptime(
                        date_str, "%d/%b/%Y:%H:%M:%S %z")
                    artist_name = match.group(2).split('/')[2]
                    file_path = match.group(2).replace(
                        '%20', ' ').replace('%7C', '|').replace('%22', '"').replace('%27', "'").replace('%2C', ',').replace('%28', '(').replace('%29', ')')
                    key = self.find_song_from_path(metadata_dict, file_path)
                    value = date_formated
                    if artist_name not in self.dict:
                        self.dict[artist_name] = {}
                    if key not in self.dict[artist_name]:
                        self.dict[artist_name][key] = []
                    self.dict[artist_name][key].append(value)

    def find_song_from_path(self, metadata_dict, file_path):
        if file_path.startswith('/'):
            file_path = file_path[1:]
        # remove extension of filepath
        file_path = file_path.split('.')[0]
        for song, metadata in metadata_dict.items():
            if metadata.get('file_path') == file_path:
                return song
        return None
