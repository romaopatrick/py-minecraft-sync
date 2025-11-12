import glob
import os
import platform

from dotenv import load_dotenv

import compress
import sync

WIN_SAVES_PATH = "C:\\Users\\patri\\AppData\\Roaming\\.minecraft_server/p3tworld"
LINUX_SAVES_PATH = "/home/p3t/.minecraft_server/p3tworld"
PLATFORM = platform.uname().system.lower()


PATH = "./backup.zip"
REMOTE_PATH = "/backup.zip"


def main():
    load_dotenv()

    saves_folder = LINUX_SAVES_PATH if 'linux' in PLATFORM else WIN_SAVES_PATH

    files_list = glob.glob(os.path.join(saves_folder, '*'))

    local_mtime = -1

    if files_list:
        latest_file = max(files_list, key=os.path.getmtime)
        local_mtime = os.path.getmtime(os.path.join(latest_file))


    output = compress.zip_folder(saves_folder, output_path=PATH)
    sync.sync_file(output, REMOTE_PATH, local_mtime=local_mtime)

    compress.unzip_file(output, saves_folder)



if __name__ == "__main__":
    main()
