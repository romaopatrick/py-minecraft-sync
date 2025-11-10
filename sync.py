import os

import dropbox
import dropbox.exceptions
import dropbox.files
from dotenv import load_dotenv

# === CONFIGURAÇÕES ===
load_dotenv()

ACCESS_TOKEN = os.getenv("DROPBOX_TOKEN") or "SEU_TOKEN_AQUI"

dbx = dropbox.Dropbox(ACCESS_TOKEN)


def upload_file(local_path: str, remote_path: str):
    """Faz upload do arquivo local para o Dropbox."""
    if not os.path.exists(local_path):
        print(f"❌ Arquivo local '{local_path}' não encontrado.")
        return

    with open(local_path, "rb") as f:
        print(f"⬆️  Enviando '{local_path}' para o Dropbox...")
        dbx.files_upload(f.read(), remote_path, mode=dropbox.files.WriteMode.overwrite)
    print("✅ Upload concluído!")


def download_file(local_path: str, remote_path: str):
    """Faz download do arquivo do Dropbox, sobrescrevendo localmente."""
    try:
        print(f"⬇️  Baixando '{remote_path}' do Dropbox...")
        _, res = dbx.files_download(remote_path)
        with open(local_path, "wb") as f:
            f.write(res.content)
        print("✅ Download concluído!")
    except dropbox.exceptions.ApiError as e:
        print(f"❌ Erro ao baixar: {e}")


def sync_file(local_path: str, remote_path: str, local_mtime: float):
    """
    Sincroniza o backup:
    - Se o arquivo local for mais novo, envia.
    - Se o arquivo remoto for mais novo, baixa.
    """
    try:
        metadata = dbx.files_get_metadata(remote_path)
        remote_mtime = metadata.client_modified.timestamp()
    except dropbox.exceptions.ApiError:
        remote_mtime = 0

    if local_mtime > remote_mtime:
        upload_file(local_path, remote_path)
    elif remote_mtime > local_mtime:
        download_file(local_path, remote_path)
    else:
        print("🔁 Arquivo já está sincronizado.")
