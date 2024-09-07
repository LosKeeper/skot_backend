import re
import datetime as dt


class NginxParser:
    def __init__(self, nginx_access_file_path):
        self.dict = {}
        self.parse(nginx_access_file_path)

    def parse(self, nginx_access_file_path):
        with open(nginx_access_file_path, 'r') as file:
            lines = file.readlines()
            for line in lines:
                if line.startswith('#'):
                    continue
                match = re.search(
                    r'\[(.*?)\].*?"GET /audio/([^/]+)/([^/]+)/([^/]+)\.(wav|aac|flac)', line)
                if match:
                    date_str = match.group(1)
                    date_formated = dt.datetime.strptime(
                        date_str, "%d/%b/%Y:%H:%M:%S %z")
                    artist_name = match.group(2)
                    file_name = match.group(4)
                    key = file_name
                    value = date_formated
                    if artist_name not in self.dict:
                        self.dict[artist_name] = {}
                    if key not in self.dict[artist_name]:
                        self.dict[artist_name][key] = []
                    self.dict[artist_name][key].append(value)


parser = NginxParser('test/nginx_access.log')
print(parser.dict["lkp"].keys().__len__())
