import os
import github
from dotenv import load_dotenv

def main():
    load_dotenv()
    github.download_folder("py-minecraft-sync", "p3tworld", destination='./p3tworld_2')

if __name__ == '__main__':
    main()