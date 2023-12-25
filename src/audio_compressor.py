import os
import subprocess
import logging
import threading
import queue
from alive_progress import alive_bar
from termcolor import colored

# Configuration du logger
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
logger = logging.getLogger(__name__)


def count_wav_files(directory):
    return sum(1 for _, _, files in os.walk(directory) for file in files if file.endswith('.wav'))


def convert_file(filename, file_path, aac_file, flac_file, q):
    command = [
        'ffmpeg', '-i', file_path,
        '-c:a', 'aac', '-b:a', '256k', aac_file,
        '-c:a', 'flac', flac_file
    ]
    subprocess.run(command, stdout=subprocess.DEVNULL,
                   stderr=subprocess.DEVNULL)
    logger.info(
        colored(f"Conversion de {os.path.basename(filename)} terminée.", 'green'))
    q.put(1)


def process_files(directory):
    total_files = count_wav_files(directory)
    q = queue.Queue()

    def update_bar(bar):
        while True:
            q.get()
            bar()
            q.task_done()

    with alive_bar(total_files, bar='filling', title='Progression totale', spinner='classic') as bar:
        threading.Thread(target=update_bar, args=(bar,), daemon=True).start()

        threads = []
        for root, _, files in os.walk(directory):
            for file in files:
                if file.endswith('.wav'):
                    file_path = os.path.join(root, file)
                    filename = os.path.splitext(file_path)[0]

                    aac_file = f"{filename}.aac"
                    flac_file = f"{filename}.flac"

                    if not (os.path.exists(aac_file) and os.path.exists(flac_file)):
                        for output_file in [aac_file, flac_file]:
                            if os.path.exists(output_file):
                                os.remove(output_file)

                        logger.info(
                            colored(f"Conversion de {os.path.basename(filename)}...", 'blue'))
                        thread = threading.Thread(target=convert_file, args=(
                            filename, file_path, aac_file, flac_file, q))
                        thread.start()
                        threads.append(thread)
                    else:
                        logger.info(colored(
                            f"Les fichiers de sortie pour {os.path.basename(filename)} existent déjà, aucune recompression nécessaire.", 'yellow'))
                        q.put(1)

        for thread in threads:
            thread.join()

        q.join()


if __name__ == "__main__":
    current_dir = os.getcwd()
    process_files(current_dir)
