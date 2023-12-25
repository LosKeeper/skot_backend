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
1. Make the .env file 
```bash
FOLDER=<path to the folder with the audio files to enceode>
```
1. Run the encoder
```bash
python main.py
```
1. Run the server using docker
```bash
docker-compose up
```

## Usage
The server will be running on port 80. You can access the files ont the url: http://localhost:80/audio/...