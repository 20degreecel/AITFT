import os
import requests
import json

def download_file(url, dest):
    print(f"Downloading {url}...")
    response = requests.get(url)
    if response.status_code == 200:
        with open(dest, 'wb') as f:
            f.write(response.content)
        print(f"Saved to {dest}")
    else:
        print(f"Failed to download {url} (Status: {response.status_code})")

data_dir = r"c:\Users\teoyo\Downloads\VSCODE\AITFT\data"
if not os.path.exists(data_dir):
    os.makedirs(data_dir)

# DAVIS dataset mirrors (DeepDTA / GraphDTA style)
# Note: The affinity file is named 'Y' without extension in some versions.
urls = {
    "davis_ligands": "https://raw.githubusercontent.com/hkmztrk/DeepDTA/master/data/davis/ligands_can.txt",
    "davis_proteins": "https://raw.githubusercontent.com/hkmztrk/DeepDTA/master/data/davis/proteins.txt",
    "davis_affinity": "https://raw.githubusercontent.com/hkmztrk/DeepDTA/master/data/davis/Y"
}

for name, url in urls.items():
    dest = os.path.join(data_dir, f"{name}.txt")
    download_file(url, dest)

print("=== DAVIS Data Collection Complete ===")
