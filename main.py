import os
import sync
import compress
from dotenv import load_dotenv

SAVES_FOLDER = "C:\\Users\\patri\\AppData\\Roaming\\.minecraft\\saves\\p3tworld"
PATH = "./backup.zip"
REMOTE_PATH = "/backup.zip"


def main():
    load_dotenv()

    output = compress.zip_folder(SAVES_FOLDER, output_path=PATH)
    sync.sync_file(output, REMOTE_PATH)

    compress.unzip_file(output, SAVES_FOLDER)



if __name__ == "__main__":
    main()
