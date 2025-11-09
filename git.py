import logging
import os

import requests




def download(repo: str, file_path: str, branch: str = 'main', destination: str = '.'):
    raw_url = f'https://raw.githubusercontent.com/{repo}/{branch}/{file_path}'
    try:
        file_name = os.path.basename(file_path)
        local_path = os.path.join(destination, file_name)

        os.makedirs(destination, exist_ok=True)


        print(f"⬇️  Baixando {file_name} de {repo}...")

        response = requests.get(raw_url, stream=True)

        if response.status_code != 200:
            print(f"❌ Erro {response.status_code}: não foi possível baixar o arquivo.")
            return
        
        with open(local_path, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
                
            print(f"✅ Download concluído: {local_path}")
        

    except Exception as e:
        print(f"erro ao efetuar download da url {raw_url} do git")
        raise e