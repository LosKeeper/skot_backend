import os
import subprocess
import threading
import queue
from alive_progress import alive_bar
from termcolor import colored


class AudioCompressor:
    def __init__(self, directory, logger, force=False):
        self.directory = directory
        self.logger = logger
        self.force = force
        self.q = queue.Queue()
        self.process_files()

    def count_wav_files(self):
        """Compte le nombre de fichiers .wav dans le répertoire spécifié.

        Returns:
            int: Le nombre de fichiers .wav dans le répertoire spécifié.
        """
        return sum(1 for _, _, files in os.walk(self.directory) for file in files if file.endswith('.wav'))

    def convert_file(self, file_name, file_path):
        """Convertit un fichier .wav en .aac et .flac.

        Args:
            file_name (str): Le nom du fichier.
            file_path (str): Le chemin du fichier.
        """
        command = [
            'ffmpeg', '-i', file_path,
            '-c:a', 'aac', '-b:a', '320k', file_name + '.aac',
            '-c:a', 'flac', file_name + '.flac'
        ]
        subprocess.run(command, stdout=subprocess.DEVNULL,
                       stderr=subprocess.DEVNULL)
        self.logger.info(
            colored(f"Conversion de {os.path.basename(file_name)} terminée.", 'green'))
        self.q.put(1)

    def update_bar(self, bar):
        """Met à jour la barre de progression.

        Args:
            bar (function): La barre de progression.
        """
        while True:
            self.q.get()
            bar()
            self.q.task_done()

    def process_files(self):
        """Parcours le répertoire spécifié et convertit les fichiers .wav en .aac et .flac récursivement.
        """
        total_files = self.count_wav_files()

        with alive_bar(total_files, bar='filling', title='Progression totale', spinner='classic') as bar:
            threading.Thread(target=self.update_bar,
                             args=(bar,), daemon=True).start()

            threads = []
            for root, _, files in os.walk(self.directory):
                for file in files:
                    if file.endswith('.wav'):
                        file_path = os.path.join(root, file)
                        file_name = os.path.splitext(file_path)[0]

                        aac_file = f"{file_name}.aac"
                        flac_file = f"{file_name}.flac"

                        if self.force or (not (os.path.exists(aac_file) and os.path.exists(flac_file))):
                            for output_file in [aac_file, flac_file]:
                                if os.path.exists(output_file):
                                    os.remove(output_file)

                            self.logger.info(
                                colored(f"Conversion de {os.path.basename(file_name)}...", 'blue'))
                            thread = threading.Thread(target=self.convert_file, args=(
                                file_name, file_path))
                            thread.start()
                            threads.append(thread)
                        else:
                            self.logger.info(colored(
                                f"Les fichiers de sortie pour {os.path.basename(file_name)} existent déjà, aucune recompression nécessaire.", 'yellow'))
                            self.q.put(1)

            for thread in threads:
                thread.join()

            self.q.join()
