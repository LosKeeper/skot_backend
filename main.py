import os
from dotenv import load_dotenv
import logging
import argparse

from src.inspect_files import MetadataGenerator
from src.audio_compressor import AudioCompressor
from src.message import MessageGenerator
from src.image_compressor import ImageCompressor

if __name__ == "__main__":
    # Configuration du logger
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
    logger = logging.getLogger(__name__)

    # Charger les variables d'environnement depuis le fichier .env
    load_dotenv()

    # Créer un parseur d'arguments
    parser = argparse.ArgumentParser(
        description="Générer les metadata et compresser les fichiers audio.")
    parser.add_argument('--folder', type=str,
                        help='Le chemin du dossier à traiter')
    parser.add_argument('--force', action='store_true',
                        help='Ecnode les fichiers audio même s\'ils existent déjà')
    parser.add_argument('--title', type=str, help='Le titre à ajouter')
    parser.add_argument('--message', type=str, help='Le message à ajouter')
    parser.add_argument('--selection', type=str, nargs=2,
                        help='Le couple de titres selectionnés')

    # Récupérer les arguments
    args = parser.parse_args()

    # Récupérer le répertoire à partir de la variable d'environnement FOLDER si --folder n'est pas spécifié
    folder_path = args.folder if args.folder else os.getenv("FOLDER")

    # Récupérer le répertoire à partir de la variable d'environnement FOLDER
    folder_path = os.getenv("FOLDER")

    if folder_path:
        AudioCompressor(folder_path, logger, args.force)
        ImageCompressor(folder_path, logger)
        metadata = MetadataGenerator(folder_path, logger)

        if args.title and args.message:
            MessageGenerator(folder_path + "/messages.json", logger).AddMessage(
                args.title, args.message)

        else:
            logger.error(
                "Le titre et/ou le message n'ont pas été spécifiés en argument.")

        if args.selection:
            # Check if titles exist in available_songs.json
            if args.selection[0] not in metadata.available_songs_json.keys():
                logger.error(
                    f"Le titre {args.selection[0]} n'existe pas dans le fichier available_songs.json.")
            elif args.selection[1] not in metadata.available_songs_json.keys():
                logger.error(
                    f"Le titre {args.selection[1]} n'existe pas dans le fichier available_songs.json.")
            else:
                MessageGenerator(folder_path + "/selection.json",
                                 logger).AddArtistSelection(args.selection)
        else:
            logger.error(
                "Les titres selectionnés n'ont pas été spécifiés en argument.")
    else:
        logger.error(
            "La variable FOLDER n'est pas définie dans le fichier .env ou n'a pas été spécifiée en argument.")
