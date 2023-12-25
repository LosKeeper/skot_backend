import os
from dotenv import load_dotenv
from src.inspect_files import generate_all_metadata
from src.audio_compressor import process_files

if __name__ == "__main__":
    # Charger les variables d'environnement depuis le fichier .env
    load_dotenv()

    # Récupérer le répertoire à partir de la variable d'environnement FOLDER
    folder_path = os.getenv("FOLDER")

    if folder_path:
        process_files(folder_path)
        generate_all_metadata(folder_path)
    else:
        print("La variable FOLDER n'est pas définie dans le fichier .env")
