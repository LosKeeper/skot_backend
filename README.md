# Spartacus Project Backend
> This is the backend for the top secret Spartacus Project. It is a simple server that encodes the audio files to mp3 and serves them to the frontend.

## Requirements
This project requires ffmpeg to be installed on the system. You can download it from [here](https://ffmpeg.org/download.html).

## Installation
1. Clone the repository
2. Install the dependencies
```bash
pip install -r requirements.txt
```
3. Make sure that ffmpeg is installed on your system
```bash
ffmpeg -version
```
4. Make the .env file (for the moment the folder have to be named "audio")
```bash
FOLDER=<path to the folder with the audio files to enceode>
```
5. Run the encoder
```bash
python main.py
```
Many arguments are available:
| Argument    | Description                                          |
| ----------- | ---------------------------------------------------- |
| --folder    | The folder to encode (if not in the .env file)       |
| --force     | Force the re-encoding of the existing files          |
| --message   | The message wanted to be added on the backend        |
| --title     | The title of the message to add                      |
| --selection | The audio files that are highlighted on the frontend |

6. Run the server using docker
```bash
docker-compose up
```

## Usage
You can access the files on the url: http://localhost:42024/<FOLDER>/...

## Web Server to upload files
You can use a webserver `web_upload.py` to upload files to the backend. It is a simple webserver that allows you to upload files to the backend using accounts. The accounts are stored in the `users.json` file.

You need to define the following environment variables in the `.env` file:
```bash
FOLDER=<path to the folder with the audio files to enceode>
```

You need to define the following environment variables in the `users.json` file:
```json
{
    "users": [
        {
            "username": <username>,
            "password": <password_hashed_in_sha256>
        },
        {
            "username": <username>,
            "password": <password_hashed_in_sha256>
        }, 
        ...
    ]
}
```

You can run the server using the following command:
```bash
gunicorn -w 4 --preload web_upload:app -D
```

