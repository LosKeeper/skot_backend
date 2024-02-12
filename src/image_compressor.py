import os
from PIL import Image
from termcolor import colored


class ImageCompressor:
    def __init__(self, directory, logger):
        self.directory = directory
        self.logger = logger
        self.process_files()

    def compress_and_save_image(self, img_input_path, img_output_path, folder_path):
        # Ouvrir l'image
        image = Image.open(img_input_path)

        # Convertir l'image en mode RGB
        image = image.convert("RGB")

        # Vérifier si la taille de l'image est déjà 700x700
        if image.size == (700, 700):
            self.logger.info(
                colored(f"L'image de {folder_path} est déjà de taille 700x700. Aucune compression nécessaire.", "yellow"))
            return

        # Redimensionner l'image à 700x700 pixels
        new_size = (700, 700)
        resized_image = image.resize(new_size)

        # Enregistrer l'image compressée
        resized_image.save(img_output_path, "jpg", optimize=True, quality=95)
        self.logger.info(
            colored(f"Compression de la cover de {folder_path} terminée.", "green"))

    def process_files(self):
        # Parcourir tous les fichiers et sous-dossiers du répertoire
        for root, _, files in os.walk(self.directory):
            for file in files:
                # Vérifier si le fichier est une image de couverture
                if file.lower() in ["cover.png", "cover.jpg"]:
                    # Chemin de l'image en entrée
                    img_input_path = os.path.join(root, file)

                    # Chemin de l'image en sortie
                    img_output_path = os.path.join(
                        root, "cover.jpg")

                    # Compresser et enregistrer l'image
                    self.compress_and_save_image(
                        img_input_path, img_output_path, root.split("/")[-1])
