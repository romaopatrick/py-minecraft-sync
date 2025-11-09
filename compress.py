import os
import zipfile
from datetime import datetime

def zip_folder(folder_path, output_path=None, include_timestamp=False):
    """
    Compresses a folder (recursively) into a .zip file.

    Parameters:
        folder_path (str): Path to the folder to compress
        output_path (str): Output .zip file path (default: same folder)
        include_timestamp (bool): Whether to add timestamp to zip filename

    Returns:
        str: Path to the created zip file
    """
    folder_path = os.path.abspath(folder_path)

    if not os.path.isdir(folder_path):
        print(f"❌ Folder '{folder_path}' not found.")
        return output_path

    folder_name = os.path.basename(folder_path.rstrip("/\\"))

    if output_path is None:
        file_name = folder_name
        if include_timestamp:
            ts = datetime.now().strftime("%Y%m%d_%H%M%S")
            file_name += f"_{ts}"
        output_path = f"{file_name}.zip"

    print(f"📦 Creating ZIP: {output_path} ...")

    with zipfile.ZipFile(output_path, "w", zipfile.ZIP_DEFLATED) as zipf:
        for root, _, files in os.walk(folder_path):
            for file in files:
                full_path = os.path.join(root, file)
                relative_path = os.path.relpath(full_path, start=folder_path)
                zipf.write(full_path, arcname=relative_path)

    print(f"✅ Folder '{folder_path}' compressed into '{output_path}'")
    return output_path

def unzip_file(zip_path: str, extract_to=None):
    zip_path = os.path.abspath(zip_path)

    if not os.path.isfile(zip_path):
        raise ValueError(f"❌ File '{zip_path}' not found.")

    if extract_to is None:
        extract_to = os.path.splitext(zip_path)[0]  # remove ".zip"

    os.makedirs(extract_to, exist_ok=True)

    print(f"📂 Extracting '{zip_path}' to '{extract_to}' ...")

    with zipfile.ZipFile(zip_path, "r") as zip_ref:
        zip_ref.extractall(extract_to)

    print(f"✅ Extracted successfully to '{extract_to}'")

    return extract_to
