import logging
import os

import requests




def download_folder(repo: str, path: str, branch="main", destination="."):
    # headers = {}
    # token =  os.environ.get("GITHUB_TOKEN")
    # if token:
    #     headers["Authorization"] = f"token {token}"

    api_url = f"https://api.github.com/repos/{repo}/contents/{path}?ref={branch}"
    response = requests.get(api_url)
    response.raise_for_status()

    items = response.json()
    if not isinstance(items, list):
        print(f"❌ Caminho '{path}' não encontrado no repositório {repo}.")
        return

    for item in items:
        item_path = os.path.join(destination, item["path"])

        if item["type"] == "file":
            os.makedirs(os.path.dirname(item_path), exist_ok=True)

            if os.path.exists(item_path):
                print(f"🔹 {item['path']} já existe, pulando...")
                continue

            print(f"⬇️  Baixando {item['path']} ({item['size']/1024:.1f} KB)...")

            file_response = requests.get(item["download_url"], headers=headers, stream=True)
            file_response.raise_for_status()

            with open(item_path, "wb") as f:
                for chunk in file_response.iter_content(chunk_size=8192):
                    f.write(chunk)

        elif item["type"] == "dir":
            download_folder(repo, item["path"], branch, destination, token)

    print("✅ Download completo!")
