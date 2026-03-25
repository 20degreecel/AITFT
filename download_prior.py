import requests
import os

url = "https://zenodo.org/records/10842004/files/chembl_33_v2.prior"
out_path = r"c:\Users\teoyo\Downloads\VSCODE\AITFT\REINVENT4\priors\chembl.prior"

def download():
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    print(f"Downloading Prior from {url}...")
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()
        with open(out_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        print(f"Saved to {out_path}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    download()
